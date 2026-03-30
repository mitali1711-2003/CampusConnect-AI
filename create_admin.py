"""
Utility script to create an admin user.
Run: python create_admin.py
"""

from models.database import get_db, init_db
from utils.auth import hash_password

def create_admin():
    init_db()
    conn = get_db()

    # Check if admin already exists
    existing = conn.execute("SELECT id FROM users WHERE username = 'admin'").fetchone()
    if existing:
        print("Admin user already exists.")
        conn.close()
        return

    hashed = hash_password('admin123')
    conn.execute(
        "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
        ('admin', 'admin@university.edu', hashed, 'admin')
    )
    conn.commit()
    conn.close()
    print("Admin user created!")
    print("  Username: admin")
    print("  Password: admin123")
    print("  (Change this password in production!)")

if __name__ == '__main__':
    create_admin()
