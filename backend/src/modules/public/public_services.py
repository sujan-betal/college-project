from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.models.user_model import User
from src.models.teacher_model import Teacher
from src.models.course_model import Department, Course
from src.models.content_model import Notice
from src.models.activity_model import AdmissionApplication
from src.models.site_model import Event, GalleryItem, SiteContent, ContactMessage
from src.modules.public.public_schemas import ContactSchema, AdmissionApplySchema
from src.utils.common_schema import api_response_success
from src.utils.status_code import StatusCode


async def _content_map(db: AsyncSession):
    rows = (await db.execute(select(SiteContent))).scalars().all()
    return {r.key: r.value for r in rows}


async def get_home(db: AsyncSession):
    students = (await db.execute(
        select(func.count()).select_from(User).where(User.role == "STUDENT", User.is_deleted == False)
    )).scalar()
    teachers = (await db.execute(
        select(func.count()).select_from(User).where(User.role == "TEACHER", User.is_deleted == False)
    )).scalar()
    programs = (await db.execute(select(func.count()).select_from(Course))).scalar()
    content = await _content_map(db)

    return api_response_success(data={
        "college_name": content.get("college_name", "AstraVidya Institute of Technology"),
        "slogan": content.get("slogan", "Ignite. Innovate. Excel."),
        "stats": {"students": students, "programs": programs, "faculty": teachers},
    })


async def get_site_content(db: AsyncSession):
    return api_response_success(data=await _content_map(db))


async def get_notices(db: AsyncSession):
    rows = (await db.execute(
        select(Notice)
        .where(Notice.is_published == 1)
        .order_by(Notice.created_at.desc())
    )).scalars().all()

    return api_response_success(data=[
        {"id": n.id, "title": n.title, "body": n.body, "audience": n.audience, "created_at": n.created_at}
        for n in rows
    ])


async def get_courses(db: AsyncSession):
    rows = (await db.execute(select(Course))).scalars().all()
    return api_response_success(data=[
        {
            "id": c.id,
            "name": c.name,
            "code": c.code,
            "duration_years": c.duration_years,
            "total_seats": c.total_seats,
            "annual_fee": float(c.annual_fee or 0),
            "department_id": c.department_id,
        }
        for c in rows
    ])


async def get_departments(db: AsyncSession):
    rows = (await db.execute(select(Department))).scalars().all()
    return api_response_success(data=[
        {"id": d.id, "name": d.name, "code": d.code, "description": d.description}
        for d in rows
    ])


async def get_faculty(db: AsyncSession):
    rows = (await db.execute(select(Teacher))).scalars().all()
    return api_response_success(data=[
        {
            "id": t.id,
            "employee_id": t.employee_id,
            "designation": t.designation,
            "department_id": t.department_id,
            "is_department_head": bool(t.is_department_head),
        }
        for t in rows
    ])


async def get_events(db: AsyncSession):
    rows = (await db.execute(select(Event).order_by(Event.event_date.desc()))).scalars().all()
    return api_response_success(data=[
        {"id": e.id, "title": e.title, "description": e.description, "event_date": e.event_date, "venue": e.venue}
        for e in rows
    ])


async def get_gallery(db: AsyncSession):
    rows = (await db.execute(select(GalleryItem).order_by(GalleryItem.created_at.desc()))).scalars().all()
    return api_response_success(data=[
        {"id": g.id, "title": g.title, "album": g.album, "image_url": g.image_url}
        for g in rows
    ])


async def apply_admission(db: AsyncSession, payload: AdmissionApplySchema):
    application = AdmissionApplication(
        applicant_name=payload.applicant_name,
        email=payload.email,
        phone=payload.phone,
        course_id=payload.course_id,
    )

    db.add(application)
    await db.commit()

    return api_response_success(
        data={"id": application.id},
        message="Application submitted",
        status_code=StatusCode.create,
    )


async def send_contact_message(db: AsyncSession, payload: ContactSchema):
    row = ContactMessage(name=payload.name, email=payload.email, message=payload.message)

    db.add(row)
    await db.commit()

    return api_response_success(
        data={"id": row.id},
        message="Message sent",
        status_code=StatusCode.create,
    )