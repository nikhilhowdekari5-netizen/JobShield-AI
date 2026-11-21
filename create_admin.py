import sqlite3
import os
from getpass import getpass
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "job_history.db")

name = input("Enter admin name: ")
email = input("Enter admin email: ").strip().lower()
password = getpass("Enter admin password: ")

if len(password) < 8:
    print("Password must contain at least 8 characters.")
    raise SystemExit

conn = sqlite3.connect(DB_PATH)

try:
    conn.execute("""
        INSERT INTO users
        (name, email, password, role, created_at)
        VALUES (?, ?, ?, ?, datetime('now'))
    """, (
        name,
        email,
        generate_password_hash(password),
        "admin"
    ))

    conn.commit()
    print("Admin account created successfully!")

except sqlite3.IntegrityError:
    print("This email is already registered.")

finally:
    conn.close()