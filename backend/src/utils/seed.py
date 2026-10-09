from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.permission_model import Role

# The three roles the system needs to work. Everything else is created by an
# admin at runtime from the Roles page.
STARTING_ROLES = [
    ("ADMIN", "Full system administrator", True, True),
    ("TEACHER", "Teaching staff", False, True),
    ("STUDENT", "Enrolled student", False, True),
]


async def seed_roles(db: AsyncSession):
    existing = {r.name for r in (await db.execute(select(Role))).scalars().all()}

    for name, description, is_admin, is_system in STARTING_ROLES:
        if name not in existing:
            db.add(Role(name=name, description=description, is_admin=is_admin, is_system=is_system))

    await db.commit()