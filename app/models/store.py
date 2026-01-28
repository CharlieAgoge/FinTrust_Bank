"""In-memory / SQLite account and user store for Week 1."""
import os
import sqlite3
from pathlib import Path
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


def get_balance(username: str) -> float | None:
    """Return balance for user or None if not found."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT balance FROM accounts WHERE username = ?", (username,)
        ).fetchone()
        return float(row[0]) if row else None
    finally:
        conn.close()


def transfer(from_user: str, to_user: str, amount: float) -> tuple[bool, str]:
    """
    Transfer amount from from_user to to_user. Returns (success, message).
    Preserves integrity: amount is unchanged and balances are updated atomically.
    """
    if amount <= 0:
        return False, "Amount must be positive."
    conn = _get_conn()
    try:
        conn.execute("BEGIN IMMEDIATE")
        from_bal = get_balance(from_user)
        to_bal = get_balance(to_user)
        if from_bal is None:
            conn.rollback()
            return False, "Sender account not found."
        if to_bal is None:
            conn.rollback()
            return False, "Recipient account not found."
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


def store_balance(username: str) -> float | None:
    return get_balance(username)


def store_transfer(from_user: str, to_user: str, amount: float) -> tuple[bool, str]:
    return transfer(from_user, to_user, amount)
