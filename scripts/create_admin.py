"""
CLI script to create the first admin user.

Usage:
    python scripts/create_admin.py

Or via Flask CLI:
    flask create-admin
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from getpass import getpass
from app import create_app
from app.extensions import db
from app.models.user import User


def create_admin():
    app = create_app()
    with app.app_context():
        print("\n=== Create Admin User ===\n")

        email = input("Email: ").strip().lower()
        if not email:
            print("Error: Email is required.")
            return

        existing = User.query.filter_by(email=email).first()
        if existing:
            print(f"Error: User with email '{email}' already exists.")
            return

        display_name = input("Display name: ").strip()
        if not display_name:
            print("Error: Display name is required.")
            return

        password = getpass("Password: ")
        if len(password) < 8:
            print("Error: Password must be at least 8 characters.")
            return

        confirm = getpass("Confirm password: ")
        if password != confirm:
            print("Error: Passwords do not match.")
            return

        user = User(
            email=email,
            display_name=display_name,
            role='admin',
            is_active=True,
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        print(f"\nAdmin user '{display_name}' ({email}) created successfully!")


if __name__ == '__main__':
    create_admin()
