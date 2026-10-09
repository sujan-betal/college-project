import uuid
import logging
import os
import secrets

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from starlette.concurrency import run_in_threadpool

from src.models.user_model import User
from src.models.permission_model import UserPermission, Role
from src.models.student_model import Student
from src.models.teacher_model import Teacher
from src.models.course_model import Department, Course, Subject
from src.models.academic_model import Exam
from src.models.content_model import Notice, StudyMaterial, Assignment
from src.models.site_model import Event, GalleryItem, SiteContent, Certificate, ContactMessage
from src.models.teacher_model import Teacher, TeacherSubject
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
    RoleCreateSchema,
    RoleUpdateSchema,
    SubjectCreateSchema,
    TeacherSubjectCreateSchema,
    NoticeCreateSchema,
    EventCreateSchema,
    GalleryCreateSchema,
    SiteContentSchema,
    CertificateCreateSchema,
    FeePaymentCreateSchema,
    StudentEnrollmentSchema,
)
from src.utils.password import hash_password
from src.utils.jwt import create_reset_token
from src.utils.mailer import send_password_setup_email, FRONTEND_URI
from src.utils.common_schema import api_response_success, api_response_error
from src.utils.status_code import StatusCode

logger = logging.getLogger(__name__)


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

async def list_permission_names(db: AsyncSession):
    """Every permission name currently in use, so the UI can suggest them."""
    rows = (await db.execute(
        select(UserPermission.permission).distinct().order_by(UserPermission.permission)
    )).scalars().all()

    return api_response_success(data=sorted({(p or "").upper() for p in rows if p}))


def _clean_permissions(values) -> list[str]:
    """Accept a list or a comma/space separated string of names."""
    if values is None:
        return []

    if isinstance(values, str):
        values = values.replace(",", " ").split()

    names = {str(v or "").strip().upper() for v in values}
    names.discard("")

    if "ALL" in names:
        return ["ALL"]

    return sorted(names)


async def list_roles(db: AsyncSession):
    rows = (await db.execute(select(Role).order_by(Role.name))).scalars().all()

    counts = dict((await db.execute(
        select(User.role, func.count())
        .where(User.is_deleted == False)
        .group_by(User.role)
    )).all())

    return api_response_success(data=[
        {
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "is_admin": bool(r.is_admin),
            "is_system": bool(r.is_system),
            "user_count": int(counts.get(r.name, 0) or 0),
        }
        for r in rows
    ])


async def create_role(db: AsyncSession, payload: RoleCreateSchema, admin: User):
    name = payload.name.strip()

    existing = (await db.execute(
        select(Role).where(func.lower(Role.name) == name.lower())
    )).scalar_one_or_none()

    if existing:
        return api_response_error(
            message="Role already exists",
            status_code=StatusCode.badRequest
        )

    role = Role(
        name=name,
        description=payload.description,
        is_admin=payload.is_admin,
        is_system=False,
    )
    db.add(role)

    _audit(db, admin, "ROLE_CREATED", "ROLE", name, name)
    await db.commit()

    return api_response_success(
        data={"id": role.id, "name": role.name},
        message="Role created",
        status_code=StatusCode.create
    )


async def update_role(db: AsyncSession, role_id: int, payload: RoleUpdateSchema, admin: User):
    role = (await db.execute(select(Role).where(Role.id == role_id))).scalar_one_or_none()

    if not role:
        return api_response_error(message="Role not found", status_code=StatusCode.notFound)

    if payload.description is not None:
        role.description = payload.description

    if payload.is_admin is not None:
        # Keep at least one admin-capable role, otherwise nobody could
        # manage roles any more.
        if role.name.upper() == "ADMIN" and not payload.is_admin:
            return api_response_error(
                message="The ADMIN role must stay an admin role",
                status_code=StatusCode.badRequest
            )
        role.is_admin = payload.is_admin

    _audit(db, admin, "ROLE_UPDATED", "ROLE", role.name, role.name)
    await db.commit()

    return api_response_success(message="Role updated")


async def delete_role(db: AsyncSession, role_id: int, admin: User):
    role = (await db.execute(select(Role).where(Role.id == role_id))).scalar_one_or_none()

    if not role:
        return api_response_error(message="Role not found", status_code=StatusCode.notFound)

    if role.is_system:
        return api_response_error(
            message="Built-in roles cannot be deleted",
            status_code=StatusCode.badRequest
        )

    in_use = (await db.execute(
        select(func.count()).select_from(User)
        .where(User.role == role.name, User.is_deleted == False)
    )).scalar()

    if in_use:
        return api_response_error(
            message=f"{in_use} user(s) still hold this role",
            status_code=StatusCode.badRequest
        )

    await db.delete(role)
    _audit(db, admin, "ROLE_DELETED", "ROLE", role_id, role.name)
    await db.commit()

    return api_response_success(message="Role deleted")


async def get_user_permissions(db: AsyncSession, userid: str):
    rows = (await db.execute(
        select(UserPermission.permission).where(UserPermission.userid == userid)
    )).scalars().all()

    return api_response_success(data=sorted({(c or "").upper() for c in rows}))


async def set_permissions(db: AsyncSession, userid: str, codes: list, admin: User):
    result = await db.execute(select(User).where(User.userid == userid))
    user = result.scalar_one_or_none()

    if not user or user.is_deleted:
        return api_response_error(message="User not found", status_code=StatusCode.notFound)

    wanted = _clean_permissions(codes)

    existing = (await db.execute(
        select(UserPermission).where(UserPermission.userid == userid)
    )).scalars().all()

    for grant in existing:
        if (grant.permission or "").upper() not in wanted:
            await db.delete(grant)

    already = {(grant.permission or "").upper() for grant in existing}

    for code in wanted:
        if code not in already:
            db.add(UserPermission(
                permission=code,
                userid=userid,
                granted_by=admin.userid if admin else None,
            ))

    _audit(db, admin, "PERMISSIONS_UPDATED", "USER", userid, ",".join(sorted(wanted)))
    await db.commit()

    return sorted(wanted)


def _resolve_permission_codes(payload: CreateUserSchema, is_admin_role: bool):
    """
    Permissions are simply the names an admin typed. If nothing was given and
    the role can reach the admin portal, fall back to ALL so a new admin is
    never locked out of their own portal.
    """
    names = _clean_permissions(payload.permissions)
    return names or (["ALL"] if is_admin_role else [])


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
        query = query.where(func.lower(User.role) == role.strip().lower())

    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    users = result.scalars().all()

    # One query for every page of grants, to avoid an N+1 lookup.
    grants: dict[str, list[str]] = {}
    if users:
        rows = (await db.execute(
            select(UserPermission.userid, UserPermission.permission)
            .where(UserPermission.userid.in_([u.userid for u in users]))
        )).all()
        for userid, code in rows:
            grants.setdefault(userid, []).append((code or "").upper())

    return api_response_success(
        data=[
            {
                "userid": u.userid,
                "username": u.username,
                "email": u.email,
                "role": u.role,
                "status": u.status,
                "is_reset": u.is_reset,
                "permissions": sorted(grants.get(u.userid, [])),
                "created_at": u.created_at,
            }
            for u in users
        ],
        message="Users fetched",
        pagination={"page": page, "page_size": page_size, "total": total},
    )


async def create_user(db: AsyncSession, payload: CreateUserSchema, admin: User):
    # Only compare email when one was actually supplied — comparing to None
    # would compile to "email IS NULL" and wrongly match every user with no email.
    uniqueness = select(User).where(User.username == payload.username)
    if payload.email:
        uniqueness = select(User).where(
            (User.username == payload.username) | (User.email == payload.email)
        )

    existing = await db.execute(uniqueness)

    if existing.scalar_one_or_none():
        return api_response_error(
            message="Username or email already exists",
            status_code=StatusCode.badRequest
        )

    role_name = (payload.role or "").strip()
    role_row = (await db.execute(
        select(Role).where(func.lower(Role.name) == role_name.lower())
    )).scalar_one_or_none()

    if not role_row:
        return api_response_error(
            message=f"Role '{role_name}' does not exist",
            status_code=StatusCode.badRequest
        )

    role = role_row.name

    if payload.department_id is not None:
        found = (await db.execute(
            select(Department.id).where(Department.id == payload.department_id)
        )).scalar_one_or_none()

        if not found:
            return api_response_error(
                message=f"Department {payload.department_id} not found",
                status_code=StatusCode.notFound
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

    codes = _resolve_permission_codes(payload, bool(role_row.is_admin))

    for code in codes:
        db.add(UserPermission(
            permission=code,
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

    # Email the new user a link where they choose their own password. A mail
    # failure must not undo the account that was just created.
    mail_sent, mail_error = False, ""
    nonce = secrets.token_urlsafe(24)
    user.reset_nonce = nonce
    await db.commit()

    token = create_reset_token(user.userid, user.role, nonce)

    if user.email:
        mail_sent, mail_error = await run_in_threadpool(
            send_password_setup_email, user.email, user.username, user.role, token
        )
        if not mail_sent:
            logger.warning("Welcome email failed for %s: %s", user.username, mail_error)

    return api_response_success(
        data={
            "userid": user.userid,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "permissions": codes,
            "set_password_url": f"{FRONTEND_URI.rstrip('/')}/set-password?token={token}",
            "email_sent": mail_sent,
        },
        message=(
            f"User created. Password setup link emailed to {user.email}."
            if mail_sent else
            f"User created. Could not send email ({mail_error}). "
            f"Share this link so they can set a password: "
            f"{FRONTEND_URI.rstrip('/')}/set-password?token={token}"
        ),
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
    existing = (await db.execute(
        select(Department).where(func.lower(Department.code) == code.strip().lower())
    )).scalar_one_or_none()

    if existing:
        return api_response_error(
            message="A department with that code already exists",
            status_code=StatusCode.badRequest
        )

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
    existing = (await db.execute(
        select(Course).where(func.lower(Course.code) == payload.code.strip().lower())
    )).scalar_one_or_none()

    if existing:
        return api_response_error(
            message="A course with that code already exists",
            status_code=StatusCode.badRequest
        )

    found = (await db.execute(
        select(Department.id).where(Department.id == payload.department_id)
    )).scalar_one_or_none()

    if not found:
        return api_response_error(
            message=f"Department {payload.department_id} not found",
            status_code=StatusCode.notFound
        )

    course = Course(**payload.model_dump())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return api_response_success(
        data={"id": course.id},
        message="Course created",
        status_code=StatusCode.create
    )


async def update_student_enrollment(db: AsyncSession, userid: str, payload: StudentEnrollmentSchema):
    """
    Put a student into a course/semester/section.

    Without this the student has no course_id, and the materials, assignment
    and marks queries (which filter by course) never match anything.
    """
    student = (await db.execute(
        select(Student).where(Student.userid == userid)
    )).scalar_one_or_none()

    if not student:
        return api_response_error(message="Student not found", status_code=StatusCode.notFound)

    if payload.course_id is not None:
        found = (await db.execute(
            select(Course.id).where(Course.id == payload.course_id)
        )).scalar_one_or_none()

        if not found:
            return api_response_error(
                message=f"Course {payload.course_id} not found",
                status_code=StatusCode.notFound
            )
        student.course_id = payload.course_id

    if payload.department_id is not None:
        found = (await db.execute(
            select(Department.id).where(Department.id == payload.department_id)
        )).scalar_one_or_none()

        if not found:
            return api_response_error(
                message=f"Department {payload.department_id} not found",
                status_code=StatusCode.notFound
            )
        student.department_id = payload.department_id

    if payload.semester is not None:
        student.semester = payload.semester

    if payload.section is not None:
        student.section = payload.section

    await db.commit()

    return api_response_success(
        data={
            "course_id": student.course_id,
            "semester": student.semester,
            "section": student.section,
            "department_id": student.department_id,
        },
        message="Student enrolled",
    )


# --------------------------------------------------
# Academic setup (subjects, teacher assignments)
# --------------------------------------------------

async def list_subjects(db: AsyncSession):
    rows = (await db.execute(
        select(Subject, Course.name).join(Course, Course.id == Subject.course_id).order_by(Subject.name)
    )).all()

    return api_response_success(data=[
        {
            "id": s.id, "name": s.name, "code": s.code,
            "course_id": s.course_id, "course_name": cname,
            "credits": s.credits, "semester": s.semester,
        }
        for s, cname in rows
    ])


async def create_subject(db: AsyncSession, payload: SubjectCreateSchema):
    existing = (await db.execute(
        select(Subject).where(func.lower(Subject.code) == payload.code.strip().lower())
    )).scalar_one_or_none()

    if existing:
        return api_response_error(message="Subject code already exists", status_code=StatusCode.badRequest)

    found = (await db.execute(select(Course.id).where(Course.id == payload.course_id))).scalar_one_or_none()
    if not found:
        return api_response_error(message=f"Course {payload.course_id} not found", status_code=StatusCode.notFound)

    subject = Subject(**payload.model_dump())
    db.add(subject)
    await db.commit()
    await db.refresh(subject)

    return api_response_success(
        data={"id": subject.id, "name": subject.name, "code": subject.code},
        message="Subject created",
        status_code=StatusCode.create,
    )


async def list_teacher_subjects(db: AsyncSession):
    rows = (await db.execute(
        select(TeacherSubject, Subject.name, Subject.code, User.username)
        .join(Subject, Subject.id == TeacherSubject.subject_id)
        .join(Teacher, Teacher.id == TeacherSubject.teacher_id)
        .join(User, User.userid == Teacher.userid)
        .order_by(User.username)
    )).all()

    return api_response_success(data=[
        {
            "id": ts.id,
            "teacher_id": ts.teacher_id,
            "teacher_name": uname,
            "subject_id": ts.subject_id,
            "subject_name": sname,
            "subject_code": scode,
            "section": ts.section,
            "academic_year": ts.academic_year,
        }
        for ts, sname, scode, uname in rows
    ])


async def assign_teacher_subject(db: AsyncSession, payload: TeacherSubjectCreateSchema):
    teacher = (await db.execute(select(Teacher).where(Teacher.id == payload.teacher_id))).scalar_one_or_none()
    if not teacher:
        return api_response_error(message="Teacher not found", status_code=StatusCode.notFound)

    subject = (await db.execute(select(Subject).where(Subject.id == payload.subject_id))).scalar_one_or_none()
    if not subject:
        return api_response_error(message="Subject not found", status_code=StatusCode.notFound)

    existing = (await db.execute(
        select(TeacherSubject).where(
            TeacherSubject.teacher_id == payload.teacher_id,
            TeacherSubject.subject_id == payload.subject_id,
            TeacherSubject.section == payload.section,
        )
    )).scalar_one_or_none()

    if existing:
        return api_response_error(
            message="Teacher already teaches this subject for this section",
            status_code=StatusCode.badRequest
        )

    row = TeacherSubject(
        teacher_id=payload.teacher_id,
        subject_id=payload.subject_id,
        course_id=subject.course_id,
        section=payload.section,
        academic_year=payload.academic_year,
    )
    db.add(row)
    await db.commit()

    return api_response_success(
        data={"id": row.id},
        message="Subject assigned to teacher",
        status_code=StatusCode.create,
    )


# --------------------------------------------------
# Notices
# --------------------------------------------------

async def create_notice(db: AsyncSession, payload: NoticeCreateSchema, admin: User):
    notice = Notice(
        title=payload.title,
        body=payload.body,
        audience=payload.audience,
        is_published=payload.is_published,
        created_by=admin.userid,
    )
    db.add(notice)
    await db.commit()

    return api_response_success(
        data={"id": notice.id}, message="Notice posted", status_code=StatusCode.create
    )


# --------------------------------------------------
# Public site content
# --------------------------------------------------

async def create_event(db: AsyncSession, payload: EventCreateSchema):
    event = Event(**payload.model_dump())
    db.add(event)
    await db.commit()

    return api_response_success(
        data={"id": event.id}, message="Event created", status_code=StatusCode.create
    )


async def list_public_events(db: AsyncSession):
    rows = (await db.execute(select(Event).order_by(Event.event_date.desc()))).scalars().all()
    return api_response_success(data=[
        {"id": e.id, "title": e.title, "description": e.description,
         "event_date": e.event_date, "venue": e.venue}
        for e in rows
    ])


async def list_public_gallery(db: AsyncSession):
    rows = (await db.execute(select(GalleryItem).order_by(GalleryItem.id.desc()))).scalars().all()
    return api_response_success(data=[
        {"id": g.id, "title": g.title, "album": g.album, "image_url": g.image_url}
        for g in rows
    ])


async def list_public_certificates(db: AsyncSession):
    rows = (await db.execute(select(Certificate).order_by(Certificate.id.desc()))).scalars().all()
    return api_response_success(data=[
        {"id": c.id, "student_id": c.student_id, "title": c.title,
         "certificate_no": c.certificate_no, "issued_on": c.issued_on}
        for c in rows
    ])


async def create_gallery_item(db: AsyncSession, payload: GalleryCreateSchema):
    item = GalleryItem(**payload.model_dump())
    db.add(item)
    await db.commit()

    return api_response_success(
        data={"id": item.id}, message="Gallery item added", status_code=StatusCode.create
    )


async def set_site_content(db: AsyncSession, payload: SiteContentSchema):
    row = (await db.execute(
        select(SiteContent).where(SiteContent.key == payload.key)
    )).scalar_one_or_none()

    if row:
        row.value = payload.value
    else:
        db.add(SiteContent(key=payload.key, value=payload.value))

    await db.commit()
    return api_response_success(message="Content saved")


async def create_certificate(db: AsyncSession, payload: CertificateCreateSchema):
    found = (await db.execute(
        select(Student.id).where(Student.id == payload.student_id)
    )).scalar_one_or_none()

    if not found:
        return api_response_error(message=f"Student {payload.student_id} not found", status_code=StatusCode.notFound)

    row = Certificate(**payload.model_dump())
    db.add(row)
    await db.commit()

    return api_response_success(
        data={"id": row.id}, message="Certificate issued", status_code=StatusCode.create
    )


async def record_fee_payment(db: AsyncSession, payload: FeePaymentCreateSchema):
    found = (await db.execute(
        select(Student.id).where(Student.id == payload.student_id)
    )).scalar_one_or_none()

    if not found:
        return api_response_error(message=f"Student {payload.student_id} not found", status_code=StatusCode.notFound)

    duplicate = (await db.execute(
        select(FeePayment.id).where(FeePayment.receipt_no == payload.receipt_no)
    )).scalar_one_or_none()

    if duplicate:
        return api_response_error(message="Receipt number already used", status_code=StatusCode.badRequest)

    row = FeePayment(**payload.model_dump())
    db.add(row)
    await db.commit()

    return api_response_success(
        data={"id": row.id}, message="Payment recorded", status_code=StatusCode.create
    )


async def list_fee_payments(db: AsyncSession):
    rows = (await db.execute(
        select(FeePayment, Student.roll_no)
        .join(Student, Student.id == FeePayment.student_id)
        .order_by(FeePayment.id.desc())
    )).all()

    return api_response_success(data=[
        {
            "id": p.id, "student_id": p.student_id, "roll_no": roll,
            "amount": float(p.amount or 0), "receipt_no": p.receipt_no,
            "payment_mode": p.payment_mode, "paid_on": p.paid_on,
        }
        for p, roll in rows
    ])


async def list_messages(db: AsyncSession):
    rows = (await db.execute(
        select(ContactMessage).order_by(ContactMessage.created_at.desc()).limit(100)
    )).scalars().all()

    return api_response_success(data=[
        {
            "id": m.id, "name": m.name, "email": m.email,
            "message": m.message, "created_at": m.created_at,
        }
        for m in rows
    ])


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
    found = (await db.execute(
        select(Course.id).where(Course.id == payload.course_id)
    )).scalar_one_or_none()

    if not found:
        return api_response_error(
            message=f"Course {payload.course_id} not found",
            status_code=StatusCode.notFound
        )

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
    if payload.course_id is not None:
        found = (await db.execute(
            select(Course.id).where(Course.id == payload.course_id)
        )).scalar_one_or_none()

        if not found:
            return api_response_error(
                message=f"Course {payload.course_id} not found",
                status_code=StatusCode.notFound
            )

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