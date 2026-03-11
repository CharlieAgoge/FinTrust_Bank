"""In-memory / SQLite account and user store for Week 1."""
import os
import sqlite3
from pathlib import Path
from typing import Optional, Tuple
from werkzeug.security import check_password_hash, generate_password_hash

# SQLite path: instance/ under project root (FinTrust_Bank/)
def _db_path():
    root = Path(__file__).resolve().parent.parent.parent  # app/models -> app -> repo root
    base = Path(os.environ.get("FINTRUST_DB_DIR", root)) / "instance"
    base.mkdir(parents=True, exist_ok=True)
    return str(base / "fintrust.sqlite")


def _get_conn():
    return sqlite3.connect(_db_path())


def init_db():
    """Create tables if not present."""
    conn = _get_conn()
    try:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS accounts (
                username TEXT PRIMARY KEY,
                balance REAL NOT NULL DEFAULT 0,
                FOREIGN KEY (username) REFERENCES users(username)
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS transfers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user TEXT NOT NULL,
                to_user TEXT NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (from_user) REFERENCES users(username),
                FOREIGN KEY (to_user) REFERENCES users(username)
            )"""
        )
        conn.commit()
    finally:
        conn.close()


def seed_demo():
    """Insert demo users and balances if none exist."""
    conn = _get_conn()
    try:
        cur = conn.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] > 0:
            return
        for username, password, balance in [
            ("student", "demopassword", 1000.0),
            ("alice", "alice123", 500.0),
            ("bob", "bob123", 250.0),
        ]:
            conn.execute(
                "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
                (username, generate_password_hash(password, method="scrypt")),
            )
            conn.execute(
                "INSERT OR REPLACE INTO accounts (username, balance) VALUES (?, ?)",
                (username, balance),
            )
        conn.commit()
    finally:
        conn.close()


def verify_user(username: str, password: str) -> bool:
    """Return True if username and password match."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT password_hash FROM users WHERE username = ?", (username,)
        ).fetchone()
        if not row:
            return False
        return check_password_hash(row[0], password)
    finally:
        conn.close()


def get_balance(username: str) -> Optional[float]:
    """Return balance for user or None if not found."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT balance FROM accounts WHERE username = ?", (username,)
        ).fetchone()
        return float(row[0]) if row else None
    finally:
        conn.close()


def _validate_transfer_inputs(from_user: str, to_user: str, amount: float) -> Tuple[bool, str]:
    """Validate transfer inputs. Returns (valid, error_message)."""
    if not from_user or not isinstance(from_user, str):
        return False, "Invalid sender."
    if not to_user or not isinstance(to_user, str):
        return False, "Invalid recipient."
    from_user = from_user.strip()
    to_user = to_user.strip()
    if not from_user or not to_user:
        return False, "Sender and recipient are required."
    if from_user == to_user:
        return False, "Cannot transfer to yourself."
    try:
        amt = float(amount)
    except (TypeError, ValueError):
        return False, "Amount must be a valid number."
    if amt <= 0:
        return False, "Amount must be positive."
    if amt != amt or amt == float("inf"):  # NaN or infinity
        return False, "Amount must be a finite number."
    return True, ""


def transfer(from_user: str, to_user: str, amount: float) -> Tuple[bool, str]:
    """
    Transfer amount from from_user to to_user. Returns (success, message).
    Preserves integrity: amount is unchanged and balances are updated atomically.
    Balance check and updates run in the same transaction to prevent race conditions.
    """
    ok, err = _validate_transfer_inputs(from_user, to_user, amount)
    if not ok:
        return False, err
    from_user = from_user.strip()
    to_user = to_user.strip()
    amount = float(amount)
    conn = _get_conn()
    try:
        conn.execute("BEGIN IMMEDIATE")
        # Balance check within same transaction/connection - prevents race condition.
        # Using get_balance() would open separate connections, allowing concurrent
        # transfers to bypass balance checks between read and update.
        from_row = conn.execute(
            "SELECT balance FROM accounts WHERE username = ?", (from_user,)
        ).fetchone()
        to_row = conn.execute(
            "SELECT balance FROM accounts WHERE username = ?", (to_user,)
        ).fetchone()
        if from_row is None:
            conn.rollback()
            return False, "Sender account not found."
        if to_row is None:
            conn.rollback()
            return False, "Recipient account not found."
        from_bal = float(from_row[0])
        if from_bal < amount:
            conn.rollback()
            return False, "Insufficient balance."
        conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE username = ?",
            (amount, from_user),
        )
        conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE username = ?",
            (amount, to_user),
        )
        conn.execute(
            "INSERT INTO transfers (from_user, to_user, amount) VALUES (?, ?, ?)",
            (from_user, to_user, amount),
        )
        conn.commit()
        return True, f"Transferred £{amount:.2f} to {to_user}."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


# Singleton-style helpers used by routes
def store_verify(username: str, password: str) -> bool:
    return verify_user(username, password)


def store_balance(username: str) -> Optional[float]:
    return get_balance(username)


def store_transfer(from_user: str, to_user: str, amount: float) -> Tuple[bool, str]:
    return transfer(from_user, to_user, amount)
