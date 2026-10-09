"""Create or update the ADMIN account.

Usage:
    python scripts/create_admin.py
    python scripts/create_admin.py --username admin --password "Admin@1234"

Safe to re-run: if the username or email already exists it resets the
password and reactivates the account instead of failing.
"""

import argparse
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select

from src.config.database import SessionLocal
from src.models.user_model import User
from src.models.permission_model import UserPermission
from src.utils.password import hash_password


DEFAULT_USERNAME = "admin"
DEFAULT_EMAIL = "admin@astravidya.edu"
DEFAULT_PASSWORD = "Admin@1234"


async def create_admin(username: str, email: str, password: str):
    async with SessionLocal() as db:
        result = await db.execute(
            select(User).where((User.username == username) | (User.email == email))
        )
        user = result.scalar_one_or_none()

        if user:
            user.password = hash_password(password)
            user.role = "ADMIN"
            user.status = "ACTIVE"
            user.is_reset = False
            user.is_deleted = False
            action = "updated"
        else:
            user = User(
                username=username,
                email=email,
                role="ADMIN",
                status="ACTIVE",
                password=hash_password(password),
                is_reset=False,
            )
            db.add(user)
            action = "created"

        await db.flush()

        all_permission = (await db.execute(
            select(UserPermission).where(
                UserPermission.userid == user.userid,
                UserPermission.permission == "ALL",
            )
        )).scalar_one_or_none()

        if not all_permission:
            db.add(UserPermission(permission="ALL", userid=user.userid))

        await db.commit()

        print(f"Admin {action} with full access (ALL).")
        print(f"  username: {username}")
        print(f"  email:    {email}")
        print(f"  password: {password}")


def main():
    parser = argparse.ArgumentParser(description="Bootstrap the ADMIN account")
    parser.add_argument("--username", default=DEFAULT_USERNAME)
    parser.add_argument("--email", default=DEFAULT_EMAIL)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    args = parser.parse_args()

    asyncio.run(create_admin(args.username, args.email, args.password))


if __name__ == "__main__":
    main()