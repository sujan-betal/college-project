from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.middleware.auth import authorization
from src.modules.admin import admin_services
from src.modules.admin.admin_schemas import (
    CreateUserSchema,
    UpdateUserStatusSchema,
    SetPermissionsSchema,
    DepartmentCreateSchema,
    CourseCreateSchema,
    FeeStructureCreateSchema,
    ExamCreateSchema,
    StatusUpdateSchema,
)
from src.utils.common_schema import api_response_success

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def scoped(*permissions: str):
    """ADMIN-only endpoint that also requires the given permissions."""
    return authorization(
        allowed_roles=["ADMIN"],
        required_permissions=list(permissions),
    )


# --------------------------------------------------
# Permissions
# --------------------------------------------------

@router.get("/permissions")
async def get_permissions(db: AsyncSession = Depends(get_db), user=Depends(scoped("USER_VIEW"))):
    return await admin_services.list_permissions(db)


@router.get("/users/{userid}/permissions")
async def get_permissions_of_user(
    userid: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("USER_VIEW")),
):
    return await admin_services.get_user_permissions(db, userid)


@router.put("/users/{userid}/permissions")
async def put_permissions_of_user(
    userid: str,
    payload: SetPermissionsSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("USER_UPDATE")),
):
    granted = await admin_services.set_permissions(db, userid, payload.permissions, user)

    if isinstance(granted, dict):
        return granted

    return api_response_success(data=granted, message="Permissions updated")


# --------------------------------------------------
# Users
# --------------------------------------------------

@router.get("/users")
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = Query(""),
    role: str = Query(None),
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("USER_VIEW")),
):
    return await admin_services.list_users(db, page, page_size, search, role)


@router.post("/users")
async def create_user(
    payload: CreateUserSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("USER_CREATE")),
):
    return await admin_services.create_user(db, payload, user)


@router.put("/users/{userid}/status")
async def update_status(
    userid: str,
    payload: UpdateUserStatusSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("USER_UPDATE")),
):
    return await admin_services.update_user_status(db, userid, payload, user)


@router.delete("/users/{userid}")
async def delete_user(
    userid: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("USER_DELETE")),
):
    return await admin_services.delete_user(db, userid, user)


@router.get("/stats")
async def get_stats(
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("USER_VIEW")),
):
    return await admin_services.stats(db)


# --------------------------------------------------
# Departments
# --------------------------------------------------

@router.get("/departments")
async def get_departments(db: AsyncSession = Depends(get_db), user=Depends(scoped("COURSE_VIEW"))):
    return await admin_services.list_departments(db)


@router.post("/departments")
async def post_department(
    payload: DepartmentCreateSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("COURSE_MANAGE")),
):
    return await admin_services.create_department(db, payload.name, payload.code, payload.description)


# --------------------------------------------------
# Courses
# --------------------------------------------------

@router.get("/courses")
async def get_courses(db: AsyncSession = Depends(get_db), user=Depends(scoped("COURSE_VIEW"))):
    return await admin_services.list_courses(db)


@router.post("/courses")
async def post_course(
    payload: CourseCreateSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("COURSE_MANAGE")),
):
    return await admin_services.create_course(db, payload)


# --------------------------------------------------
# Admissions
# --------------------------------------------------

@router.get("/admissions")
async def get_admissions(db: AsyncSession = Depends(get_db), user=Depends(scoped("ADMISSION_VIEW"))):
    return await admin_services.list_admissions(db)


@router.put("/admissions/{app_id}/status")
async def admission_status(
    app_id: int,
    payload: StatusUpdateSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("ADMISSION_MANAGE")),
):
    return await admin_services.update_admission_status(db, app_id, payload.status)


# --------------------------------------------------
# Fees
# --------------------------------------------------

@router.get("/fees")
async def get_fees(db: AsyncSession = Depends(get_db), user=Depends(scoped("FEE_VIEW"))):
    return await admin_services.list_fee_structures(db)


@router.post("/fees")
async def post_fee(
    payload: FeeStructureCreateSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("FEE_MANAGE")),
):
    return await admin_services.create_fee_structure(db, payload)


# --------------------------------------------------
# Exams
# --------------------------------------------------

@router.get("/exams")
async def get_exams(db: AsyncSession = Depends(get_db), user=Depends(scoped("EXAM_VIEW"))):
    return await admin_services.list_exams(db)


@router.post("/exams")
async def post_exam(
    payload: ExamCreateSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("EXAM_MANAGE")),
):
    return await admin_services.create_exam(db, payload)


# --------------------------------------------------
# Notices
# --------------------------------------------------

@router.get("/notices")
async def get_notices(db: AsyncSession = Depends(get_db), user=Depends(scoped("NOTICE_VIEW"))):
    return await admin_services.list_notices(db)


# --------------------------------------------------
# Content
# --------------------------------------------------

@router.get("/content")
async def get_content(db: AsyncSession = Depends(get_db), user=Depends(scoped("CONTENT_VIEW"))):
    return await admin_services.list_content(db)


# --------------------------------------------------
# Leave
# --------------------------------------------------

@router.get("/leave")
async def get_leave(db: AsyncSession = Depends(get_db), user=Depends(scoped("LEAVE_VIEW"))):
    return await admin_services.list_leave(db)


@router.put("/leave/{leave_id}/status")
async def leave_status(
    leave_id: int,
    payload: StatusUpdateSchema,
    db: AsyncSession = Depends(get_db),
    user=Depends(scoped("LEAVE_APPROVE")),
):
    return await admin_services.update_leave_status(db, leave_id, payload.status, user)


# --------------------------------------------------
# Reports & Audit
# --------------------------------------------------

@router.get("/reports")
async def get_reports(db: AsyncSession = Depends(get_db), user=Depends(scoped("REPORT_VIEW"))):
    return await admin_services.reports(db)


@router.get("/audit-logs")
async def get_audit_logs(db: AsyncSession = Depends(get_db), user=Depends(scoped("AUDIT_VIEW"))):
    return await admin_services.audit_logs(db)