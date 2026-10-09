from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.permission_model import Permission, RoleTemplate


PERMISSIONS = [
    ("ALL", "System", "all", "Full access to everything"),
    ("USER_VIEW", "Users", "view", "View users"),
    ("USER_CREATE", "Users", "create", "Create admins, teachers, students"),
    ("USER_UPDATE", "Users", "update", "Edit users and activate/deactivate"),
    ("USER_DELETE", "Users", "delete", "Delete users"),
    ("COURSE_VIEW", "Courses", "view", "View departments and courses"),
    ("COURSE_MANAGE", "Courses", "manage", "Create departments and courses"),
    ("ADMISSION_VIEW", "Admissions", "view", "View admission applications"),
    ("ADMISSION_MANAGE", "Admissions", "manage", "Approve or reject admissions"),
    ("FEE_VIEW", "Fees", "view", "View fee structures"),
    ("FEE_MANAGE", "Fees", "manage", "Create fee structures"),
    ("EXAM_VIEW", "Exams", "view", "View exams"),
    ("EXAM_MANAGE", "Exams", "manage", "Create exams"),
    ("NOTICE_VIEW", "Notices", "view", "View notices"),
    ("NOTICE_MANAGE", "Notices", "manage", "Post and manage notices"),
    ("CONTENT_VIEW", "Content", "view", "View materials and assignments"),
    ("CONTENT_MANAGE", "Content", "manage", "Manage materials and assignments"),
    ("LEAVE_VIEW", "Leave", "view", "View leave requests"),
    ("LEAVE_APPROVE", "Leave", "approve", "Approve or reject leave"),
    ("REPORT_VIEW", "Reports", "view", "View reports"),
    ("AUDIT_VIEW", "Audit Logs", "view", "View audit logs"),
]

ROLE_TEMPLATES = [
    ("Accountant", "Fees and payments only", ["USER_VIEW", "FEE_VIEW", "FEE_MANAGE"]),
    ("Admission Officer", "Handles admission applications", ["USER_VIEW", "ADMISSION_VIEW", "ADMISSION_MANAGE"]),
    ("Content Manager", "Materials and notices", ["CONTENT_VIEW", "CONTENT_MANAGE", "NOTICE_VIEW", "NOTICE_MANAGE"]),
    ("Exam Controller", "Exams and results", ["EXAM_VIEW", "EXAM_MANAGE", "REPORT_VIEW"]),
    ("Course Coordinator", "Departments and courses", ["COURSE_VIEW", "COURSE_MANAGE", "USER_VIEW"]),
    ("Institute Manager", "Everything except delete and audit logs", [
        "USER_VIEW", "USER_CREATE", "USER_UPDATE",
        "COURSE_VIEW", "COURSE_MANAGE",
        "ADMISSION_VIEW", "ADMISSION_MANAGE",
        "FEE_VIEW", "FEE_MANAGE",
        "EXAM_VIEW", "EXAM_MANAGE",
        "NOTICE_VIEW", "NOTICE_MANAGE",
        "CONTENT_VIEW", "CONTENT_MANAGE",
        "LEAVE_VIEW", "LEAVE_APPROVE", "REPORT_VIEW",
    ]),
]

TEMPLATE_PERMISSIONS = {name: codes for name, _desc, codes in ROLE_TEMPLATES}


async def seed_permissions(db: AsyncSession):
    existing = {p.code for p in (await db.execute(select(Permission))).scalars().all()}

    for code, module, action, description in PERMISSIONS:
        if code not in existing:
            db.add(Permission(code=code, module=module, action=action, description=description))

    await db.commit()


async def seed_role_templates(db: AsyncSession):
    existing = {t.name for t in (await db.execute(select(RoleTemplate))).scalars().all()}

    for name, description, _codes in ROLE_TEMPLATES:
        if name not in existing:
            db.add(RoleTemplate(name=name, description=description))

    await db.commit()