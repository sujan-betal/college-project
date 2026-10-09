from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.user_model import User
from src.models.student_model import Student
from src.models.academic_model import Attendance, Marks
from src.models.content_model import Notice
from src.modules.student.student_schemas import UpdateStudentProfileSchema
from src.utils.common_schema import api_response_success, api_response_error
from src.utils.status_code import StatusCode


async def get_profile(db: AsyncSession, user: User):
    result = await db.execute(select(Student).where(Student.userid == user.userid))
    student = result.scalar_one_or_none()

    if not student:
        return api_response_error(message="Student profile not found", status_code=StatusCode.notFound)

    return api_response_success(
        data={
            "userid": user.userid,
            "username": user.username,
            "email": user.email,
            "roll_no": student.roll_no,
            "department_id": student.department_id,
            "course_id": student.course_id,
            "semester": student.semester,
            "section": student.section,
            "guardian_phone": student.guardian_phone,
        },
        message="Profile fetched",
    )


async def update_profile(db: AsyncSession, user: User, payload: UpdateStudentProfileSchema):
    result = await db.execute(select(Student).where(Student.userid == user.userid))
    student = result.scalar_one_or_none()

    if not student:
        return api_response_error(message="Student profile not found", status_code=StatusCode.notFound)

    if payload.guardian_phone is not None:
        student.guardian_phone = payload.guardian_phone
    if payload.section is not None:
        student.section = payload.section

    await db.commit()

    return api_response_success(message="Profile updated")


async def get_attendance(db: AsyncSession, user: User):
    result = await db.execute(
        select(Attendance)
        .join(Student, Student.id == Attendance.student_id)
        .where(Student.userid == user.userid)
        .order_by(Attendance.date.desc())
    )
    records = result.scalars().all()

    return api_response_success(
        data=[
            {"subject_id": r.subject_id, "date": r.date, "status": r.status}
            for r in records
        ],
        message="Attendance fetched",
    )


async def get_marks(db: AsyncSession, user: User):
    result = await db.execute(
        select(Marks)
        .join(Student, Student.id == Marks.student_id)
        .where(Student.userid == user.userid)
    )
    marks = result.scalars().all()

    return api_response_success(
        data=[
            {
                "exam_id": m.exam_id,
                "subject_id": m.subject_id,
                "marks_obtained": m.marks_obtained,
                "marks_total": m.marks_total,
            }
            for m in marks
        ],
        message="Marks fetched",
    )


async def get_notices(db: AsyncSession, user: User):
    result = await db.execute(
        select(Notice).where(Notice.is_published == 1).order_by(Notice.created_at.desc())
    )
    notices = result.scalars().all()

    return api_response_success(
        data=[{"id": n.id, "title": n.title, "body": n.body, "audience": n.audience, "created_at": n.created_at} for n in notices],
        message="Notices fetched",
    )


from src.models.activity_model import FeeStructure, FeePayment
from src.models.course_model import Subject
from src.models.content_model import StudyMaterial, Assignment
from src.models.site_model import Certificate


async def get_fees(db: AsyncSession, user: User):
    result = await db.execute(select(Student).where(Student.userid == user.userid))
    student = result.scalar_one_or_none()
    if not student:
        return api_response_error(message="Student profile not found", status_code=StatusCode.notFound)

    structures = (await db.execute(select(FeeStructure).where(FeeStructure.course_id == student.course_id))).scalars().all()
    payments = (await db.execute(select(FeePayment).where(FeePayment.student_id == student.id).order_by(FeePayment.paid_on.desc()))).scalars().all()

    return api_response_success(data={
        "fee_structure": [{"id": f.id, "head": f.head, "amount": float(f.amount or 0), "due_date": f.due_date} for f in structures],
        "payments": [{"id": p.id, "amount": float(p.amount or 0), "receipt_no": p.receipt_no, "payment_mode": p.payment_mode, "paid_on": p.paid_on} for p in payments],
    })


async def get_materials(db: AsyncSession, user: User):
    result = await db.execute(select(Student).where(Student.userid == user.userid))
    student = result.scalar_one_or_none()
    if not student:
        return api_response_error(message="Student profile not found", status_code=StatusCode.notFound)

    rows = (await db.execute(
        select(StudyMaterial)
        .join(Subject, Subject.id == StudyMaterial.subject_id)
        .where(Subject.course_id == student.course_id)
        .order_by(StudyMaterial.created_at.desc())
    )).scalars().all()

    return api_response_success(data=[{"id": m.id, "title": m.title, "subject_id": m.subject_id, "file_type": m.file_type, "file_url": m.file_url, "file_size": m.file_size, "created_at": m.created_at} for m in rows])


async def get_assignments(db: AsyncSession, user: User):
    result = await db.execute(select(Student).where(Student.userid == user.userid))
    student = result.scalar_one_or_none()
    if not student:
        return api_response_error(message="Student profile not found", status_code=StatusCode.notFound)

    query = (
        select(Assignment)
        .join(Subject, Subject.id == Assignment.subject_id)
        .where(Subject.course_id == student.course_id)
    )
    if student.section:
        query = query.where((Assignment.section == student.section) | (Assignment.section == None))
    rows = (await db.execute(query.order_by(Assignment.due_date))).scalars().all()

    return api_response_success(data=[{"id": a.id, "title": a.title, "description": a.description, "subject_id": a.subject_id, "section": a.section, "due_date": a.due_date} for a in rows])


async def get_certificates(db: AsyncSession, user: User):
    result = await db.execute(select(Student).where(Student.userid == user.userid))
    student = result.scalar_one_or_none()
    if not student:
        return api_response_error(message="Student profile not found", status_code=StatusCode.notFound)

    rows = (await db.execute(select(Certificate).where(Certificate.student_id == student.id).order_by(Certificate.issued_on.desc()))).scalars().all()
    return api_response_success(data=[{"id": c.id, "title": c.title, "certificate_no": c.certificate_no, "issued_on": c.issued_on} for c in rows])
