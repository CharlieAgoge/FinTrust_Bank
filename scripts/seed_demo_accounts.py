#!/usr/bin/env python3
"""Seed demo user accounts for FinTrust Bank. Run from repo root: python scripts/seed_demo_accounts.py"""
import sys
from pathlib import Path

# Add repo root so "app" package is importable
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from app.models.store import init_db, seed_demo


def main():
    init_db()
    seed_demo()
    print("Demo accounts seeded: student/demopassword, alice/alice123, bob/bob123")


if __name__ == "__main__":
    main()
