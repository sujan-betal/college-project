import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from src.models.user_model import User
from src.models.permission_model import Permission, UserPermission, RoleTemplate
from src.models.student_model import Student
from src.models.teacher_model import Teacher
from src.models.course_model import Department, Course
from src.models.academic_model import Exam
from src.models.content_model import Notice, StudyMaterial, Assignment
from src.models.activity_model import (
    FeeStructure,
    FeePayment,
    LeaveRequest,
    AdmissionApplication,
    AuditLog,
)
from src.modules.admin.admin_schemas import (
    CreateUserSchema,
    UpdateUserStatusSchema,
    CourseCreateSchema,
    FeeStructureCreateSchema,
    ExamCreateSchema,
)
from src.utils.password import hash_password
from src.utils.common_schema import api_response_success, api_response_error
from src.utils.status_code import StatusCode


ROLE_ALIASES = {
    "SUB_ADMIN": "ADMIN",
    "SUBADMIN": "ADMIN",
    "SUPER_ADMIN": "ADMIN",
    "SUPERADMIN": "ADMIN",
}


def _normalise_role(role: str) -> str:
    role = (role or "").upper()
    return ROLE_ALIASES.get(role, role)


def _audit(db, admin, action, target_type, target_id, meta=None):
    db.add(
        AuditLog(
            userid=str(admin.userid) if admin else None,
            action=action,
            target_type=target_type,
            target_id=str(target_id) if target_id else None,
            meta=meta,
        )
    )


# --------------------------------------------------
# Permissions
# --------------------------------------------------

async def list_permissions(db: AsyncSession):
    rows = (await db.execute(
        select(Permission).order_by(Permission.module, Permission.action)
    )).scalars().all()

    templates = (await db.execute(
        select(RoleTemplate).order_by(RoleTemplate.name)
    )).scalars().all()

    from src.utils.seed import TEMPLATE_PERMISSIONS

    return api_response_success(data={
        "permissions": [
            {
                "id": p.id,
                "code": p.code,
                "module": p.module,
                "action": p.action,
                "description": p.description,
            }
            for p in rows
        ],
        "role_templates": [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "permissions": TEMPLATE_PERMISSIONS.get(t.name, []),
            }
            for t in templates
        ],
    })


async def get_user_permissions(db: AsyncSession, userid: str):
    rows = (await db.execute(
        select(Permission.code)
        .join(UserPermission, UserPermission.permissionid == Permission.id)
        .where(UserPermission.userid == userid)
    )).scalars().all()

    return api_response_success(data=sorted({(c or "").upper() for c in rows}))


async def set_permissions(db: AsyncSession, userid: str, codes: list, admin: User):
    result = await db.execute(select(User).where(User.userid == userid))
    user = result.scalar_one_or_none()

    if not user or user.is_deleted:
        return api_response_error(message="User not found", status_code=StatusCode.notFound)

    wanted = {(c or "").upper() for c in codes}

    if "ALL" in wanted:
        wanted = {"ALL"}

    catalog = {p.code: p for p in (await db.execute(select(Permission))).scalars().all()}
    id_to_code = {p.id: p.code for p in catalog.values()}

    existing = (await db.execute(
        select(UserPermission).where(UserPermission.userid == userid)
    )).scalars().all()

    for grant in existing:
        if id_to_code.get(grant.permissionid) not in wanted:
            await db.delete(grant)

    already = {id_to_code.get(grant.permissionid) for grant in existing}

    for code in wanted - already:
        permission = catalog.get(code)
        if permission:
            db.add(UserPermission(
                permissionid=permission.id,
                userid=userid,
                granted_by=admin.userid if admin else None,
            ))

    _audit(db, admin, "PERMISSIONS_UPDATED", "USER", userid, ",".join(sorted(wanted)))
    await db.commit()

    return sorted(wanted)


async def _resolve_permission_codes(db: AsyncSession, payload: CreateUserSchema):
    codes = {(c or "").upper() for c in (payload.permissions or [])}

    if payload.role_template:
        template = (await db.execute(
            select(RoleTemplate).where(RoleTemplate.name == payload.role_template)
        )).scalar_one_or_none()

        from src.utils.seed import TEMPLATE_PERMISSIONS

        if template:
            codes.update(TEMPLATE_PERMISSIONS.get(template.name, []))

    if "ALL" in codes:
        return ["ALL"]

    return sorted(codes)


# --------------------------------------------------
# Users
# --------------------------------------------------

async def list_users(db: AsyncSession, page: int = 1, page_size: int = 10, search: str = "", role: str = None):
    query = select(User).where(User.is_deleted == False)

    if search:
        query = query.where(
            or_(
                User.username.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    if role:
        query = query.where(User.role == _normalise_role(role))

    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    users = result.scalars().all()

    return api_response_success(
        data=[
            {
                "userid": u.userid,
                "username": u.username,
                "email": u.email,
                "role": u.role,
                "status": u.status,
                "is_reset": u.is_reset,
                "created_at": u.created_at,
            }
            for u in users
        ],
        message="Users fetched",
        pagination={"page": page, "page_size": page_size, "total": total},
    )


async def create_user(db: AsyncSession, payload: CreateUserSchema, admin: User):
    existing = await db.execute(
        select(User).where(
            (User.username == payload.username) | (User.email == payload.email)
        )
    )

    if existing.scalar_one_or_none():
        return api_response_error(
            message="Username or email already exists",
            status_code=StatusCode.badRequest
        )

    role = _normalise_role(payload.role)

    if role not in ("ADMIN", "TEACHER", "STUDENT"):
        return api_response_error(
            message="Invalid role",
            status_code=StatusCode.badRequest
        )

    user = User(
        username=payload.username,
        email=payload.email,
        role=role,
        status=payload.status.upper(),
        password=hash_password("Temp@1234"),
        is_reset=True,
        created_by=admin.userid,
    )

    db.add(user)
    await db.flush()

    codes = await _resolve_permission_codes(db, payload)

    if codes:
        catalog = {p.code: p for p in (await db.execute(select(Permission))).scalars().all()}

        for code in codes:
            permission = catalog.get(code)
            if permission:
                db.add(UserPermission(
                    permissionid=permission.id,
                    userid=user.userid,
                    granted_by=admin.userid,
                ))

    if role == "STUDENT":
        db.add(Student(userid=user.userid, roll_no=f"AV{uuid.uuid4().hex[:8].upper()}"))
    elif role == "TEACHER":
        db.add(Teacher(
            userid=user.userid,
            employee_id=f"EMP{uuid.uuid4().hex[:6].upper()}",
            designation=payload.designation,
            department_id=payload.department_id,
        ))

    _audit(db, admin, "USER_CREATED", "USER", user.userid, f"{role}:{user.username}")
    await db.commit()
    await db.refresh(user)

    return api_response_success(
        data={
            "userid": user.userid,
            "username": user.username,
            "role": user.role,
            "permissions": codes,
        },
        message="User created. Default password: Temp@1234",
        status_code=StatusCode.success,
    )


async def update_user_status(db: AsyncSession, userid: str, payload: UpdateUserStatusSchema, admin: User = None):
    result = await db.execute(select(User).where(User.userid == userid, User.is_deleted == False))
    user = result.scalar_one_or_none()

    if not user:
        return api_response_error(message="User not found", status_code=StatusCode.notFound)

    user.status = payload.status.upper()
    _audit(db, admin, "USER_STATUS_UPDATED", "USER", userid, user.status)
    await db.commit()

    return api_response_success(message="User status updated")


async def delete_user(db: AsyncSession, userid: str, admin: User = None):
    result = await db.execute(select(User).where(User.userid == userid))
    user = result.scalar_one_or_none()

    if not user:
        return api_response_error(message="User not found", status_code=StatusCode.notFound)

    user.is_deleted = True
    _audit(db, admin, "USER_DELETED", "USER", userid)
    await db.commit()

    return api_response_success(message="User deleted")


async def stats(db: AsyncSession):
    total_users = (await db.execute(
        select(func.count()).select_from(User).where(User.is_deleted == False)
    )).scalar()
    students = (await db.execute(
        select(func.count()).select_from(User).where(User.role == "STUDENT", User.is_deleted == False)
    )).scalar()
    teachers = (await db.execute(
        select(func.count()).select_from(User).where(User.role == "TEACHER", User.is_deleted == False)
    )).scalar()

    return api_response_success(
        data={"total_users": total_users, "students": students, "teachers": teachers},
        message="Stats fetched",
    )


# --------------------------------------------------
# Departments
# --------------------------------------------------

async def list_departments(db: AsyncSession):
    rows = (await db.execute(select(Department))).scalars().all()
    return api_response_success(data=[
        {"id": d.id, "name": d.name, "code": d.code, "description": d.description}
        for d in rows
    ])


async def create_department(db: AsyncSession, name: str, code: str, description: str = None):
    department = Department(name=name, code=code, description=description)
    db.add(department)
    await db.commit()
    return api_response_success(
        data={"id": department.id},
        message="Department created",
        status_code=StatusCode.create
    )


# --------------------------------------------------
# Courses
# --------------------------------------------------

async def list_courses(db: AsyncSession):
    rows = (await db.execute(select(Course))).scalars().all()
    return api_response_success(data=[
        {
            "id": c.id,
            "name": c.name,
            "code": c.code,
            "department_id": c.department_id,
            "duration_years": c.duration_years,
            "total_seats": c.total_seats,
            "annual_fee": float(c.annual_fee or 0),
        }
        for c in rows
    ])


async def create_course(db: AsyncSession, payload: CourseCreateSchema):
    course = Course(**payload.model_dump())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return api_response_success(
        data={"id": course.id},
        message="Course created",
        status_code=StatusCode.create
    )


# --------------------------------------------------
# Admissions
# --------------------------------------------------

async def list_admissions(db: AsyncSession):
    rows = (await db.execute(
        select(AdmissionApplication).order_by(AdmissionApplication.created_at.desc())
    )).scalars().all()
    return api_response_success(data=[
        {
            "id": a.id,
            "applicant_name": a.applicant_name,
            "email": a.email,
            "phone": a.phone,
            "course_id": a.course_id,
            "status": a.status,
            "created_at": a.created_at,
        }
        for a in rows
    ])


async def update_admission_status(db: AsyncSession, app_id: int, status: str):
    result = await db.execute(select(AdmissionApplication).where(AdmissionApplication.id == app_id))
    row = result.scalar_one_or_none()

    if not row:
        return api_response_error(message="Application not found", status_code=StatusCode.notFound)

    row.status = status.upper()
    await db.commit()

    return api_response_success(message="Application status updated")


# --------------------------------------------------
# Fees
# --------------------------------------------------

async def list_fee_structures(db: AsyncSession):
    rows = (await db.execute(select(FeeStructure))).scalars().all()
    return api_response_success(data=[
        {"id": f.id, "course_id": f.course_id, "head": f.head, "amount": float(f.amount or 0), "due_date": f.due_date}
        for f in rows
    ])


async def create_fee_structure(db: AsyncSession, payload: FeeStructureCreateSchema):
    structure = FeeStructure(**payload.model_dump())
    db.add(structure)
    await db.commit()
    return api_response_success(
        data={"id": structure.id},
        message="Fee structure created",
        status_code=StatusCode.create
    )


# --------------------------------------------------
# Exams
# --------------------------------------------------

async def list_exams(db: AsyncSession):
    rows = (await db.execute(select(Exam).order_by(Exam.created_at.desc()))).scalars().all()
    return api_response_success(data=[
        {
            "id": e.id,
            "name": e.name,
            "course_id": e.course_id,
            "semester": e.semester,
            "start_date": e.start_date,
            "is_published": e.is_published,
        }
        for e in rows
    ])


async def create_exam(db: AsyncSession, payload: ExamCreateSchema):
    exam = Exam(**payload.model_dump())
    db.add(exam)
    await db.commit()
    return api_response_success(
        data={"id": exam.id},
        message="Exam created",
        status_code=StatusCode.create
    )


# --------------------------------------------------
# Notices
# --------------------------------------------------

async def list_notices(db: AsyncSession):
    rows = (await db.execute(select(Notice).order_by(Notice.created_at.desc()))).scalars().all()
    return api_response_success(data=[
        {
            "id": n.id,
            "title": n.title,
            "body": n.body,
            "audience": n.audience,
            "is_published": n.is_published,
            "created_at": n.created_at,
        }
        for n in rows
    ])


# --------------------------------------------------
# Content
# --------------------------------------------------

async def list_content(db: AsyncSession):
    materials = (await db.execute(
        select(StudyMaterial).order_by(StudyMaterial.created_at.desc())
    )).scalars().all()
    assignments = (await db.execute(
        select(Assignment).order_by(Assignment.created_at.desc())
    )).scalars().all()

    return api_response_success(data={
        "materials": [
            {
                "id": m.id,
                "title": m.title,
                "subject_id": m.subject_id,
                "file_type": m.file_type,
                "file_url": m.file_url,
                "created_at": m.created_at,
            }
            for m in materials
        ],
        "assignments": [
            {
                "id": a.id,
                "title": a.title,
                "subject_id": a.subject_id,
                "section": a.section,
                "due_date": a.due_date,
                "created_at": a.created_at,
            }
            for a in assignments
        ],
    })


# --------------------------------------------------
# Leave
# --------------------------------------------------

async def list_leave(db: AsyncSession):
    rows = (await db.execute(
        select(LeaveRequest).order_by(LeaveRequest.created_at.desc())
    )).scalars().all()
    return api_response_success(data=[
        {
            "id": l.id,
            "userid": l.userid,
            "from_date": l.from_date,
            "to_date": l.to_date,
            "reason": l.reason,
            "status": l.status,
            "created_at": l.created_at,
        }
        for l in rows
    ])


async def update_leave_status(db: AsyncSession, leave_id: int, status: str, reviewer: User = None):
    result = await db.execute(select(LeaveRequest).where(LeaveRequest.id == leave_id))
    row = result.scalar_one_or_none()

    if not row:
        return api_response_error(message="Leave request not found", status_code=StatusCode.notFound)

    row.status = status.upper()
    row.reviewed_by = str(reviewer.userid) if reviewer else None
    await db.commit()

    return api_response_success(message="Leave status updated")


# --------------------------------------------------
# Reports & Audit
# --------------------------------------------------

async def reports(db: AsyncSession):
    total_students = (await db.execute(
        select(func.count()).select_from(User).where(User.role == "STUDENT", User.is_deleted == False)
    )).scalar()
    total_teachers = (await db.execute(
        select(func.count()).select_from(User).where(User.role == "TEACHER", User.is_deleted == False)
    )).scalar()
    total_courses = (await db.execute(select(func.count()).select_from(Course))).scalar()
    pending_admissions = (await db.execute(
        select(func.count()).select_from(AdmissionApplication).where(AdmissionApplication.status == "PENDING")
    )).scalar()
    pending_leaves = (await db.execute(
        select(func.count()).select_from(LeaveRequest).where(LeaveRequest.status == "PENDING")
    )).scalar()
    fees_collected = (await db.execute(
        select(func.coalesce(func.sum(FeePayment.amount), 0))
    )).scalar()

    return api_response_success(data={
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_courses": total_courses,
        "pending_admissions": pending_admissions,
        "pending_leaves": pending_leaves,
        "fees_collected": float(fees_collected or 0),
    })


async def audit_logs(db: AsyncSession, limit: int = 100):
    rows = (await db.execute(
        select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    )).scalars().all()
    return api_response_success(data=[
        {
            "id": a.id,
            "userid": a.userid,
            "action": a.action,
            "target_type": a.target_type,
            "target_id": a.target_id,
            "meta": a.meta,
            "created_at": a.created_at,
        }
        for a in rows
    ])