from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.user_model import User
from src.models.teacher_model import Teacher, TeacherSubject
from src.models.content_model import Notice, StudyMaterial, Assignment
from src.modules.teacher.teacher_schemas import UpdateTeacherProfileSchema, PostNoticeSchema
from src.utils.common_schema import api_response_success, api_response_error
from src.utils.status_code import StatusCode


async def get_profile(db: AsyncSession, user: User):
    result = await db.execute(select(Teacher).where(Teacher.userid == user.userid))
    teacher = result.scalar_one_or_none()

    if not teacher:
        return api_response_error(message="Teacher profile not found", status_code=StatusCode.notFound)

    return api_response_success(
        data={
            "userid": user.userid,
            "username": user.username,
            "email": user.email,
            "employee_id": teacher.employee_id,
            "designation": teacher.designation,
            "department_id": teacher.department_id,
            "is_department_head": bool(teacher.is_department_head),
        },
        message="Profile fetched",
    )


async def update_profile(db: AsyncSession, user: User, payload: UpdateTeacherProfileSchema):
    result = await db.execute(select(Teacher).where(Teacher.userid == user.userid))
    teacher = result.scalar_one_or_none()

    if not teacher:
        return api_response_error(message="Teacher profile not found", status_code=StatusCode.notFound)

    if payload.designation is not None:
        teacher.designation = payload.designation
    if payload.department_id is not None:
        teacher.department_id = payload.department_id

    await db.commit()

    return api_response_success(message="Profile updated")


async def get_subjects(db: AsyncSession, user: User):
    result = await db.execute(
        select(TeacherSubject)
        .join(Teacher, Teacher.id == TeacherSubject.teacher_id)
        .where(Teacher.userid == user.userid)
    )
    subjects = result.scalars().all()

    return api_response_success(
        data=[
            {
                "subject_id": s.subject_id,
                "course_id": s.course_id,
                "section": s.section,
                "academic_year": s.academic_year,
            }
            for s in subjects
        ],
        message="Subjects fetched",
    )


async def post_notice(db: AsyncSession, user: User, payload: PostNoticeSchema):
    notice = Notice(
        title=payload.title,
        body=payload.content,
        audience=payload.audience,
        created_by=user.userid,
        is_published=1,
    )

    db.add(notice)
    await db.commit()
    await db.refresh(notice)

    return api_response_success(data={"id": notice.id}, message="Notice posted", status_code=StatusCode.create)


from src.models.academic_model import Attendance, Marks, Exam
from src.models.activity_model import LeaveRequest
from src.models.student_model import Student


def _teacher_id(teacher):
    return teacher.id if teacher else None


async def _get_teacher(db, user):
    result = await db.execute(select(Teacher).where(Teacher.userid == user.userid))
    return result.scalar_one_or_none()


async def get_attendance(db, user):
    teacher = await _get_teacher(db, user)
    if not teacher:
        return api_response_error(message="Teacher profile not found", status_code=StatusCode.notFound)
    rows = (await db.execute(select(Attendance).where(Attendance.teacher_id == teacher.id).order_by(Attendance.date.desc()))).scalars().all()
    return api_response_success(data=[{"id": a.id, "student_id": a.student_id, "subject_id": a.subject_id, "date": a.date, "status": a.status} for a in rows])


async def mark_attendance(db, user, payload):
    teacher = await _get_teacher(db, user)
    if not teacher:
        return api_response_error(message="Teacher profile not found", status_code=StatusCode.notFound)
    for r in payload.records:
        existing = (await db.execute(
            select(Attendance).where(Attendance.student_id == r.student_id, Attendance.subject_id == r.subject_id, Attendance.date == r.date)
        )).scalar_one_or_none()
        if existing:
            existing.status = r.status
            existing.teacher_id = teacher.id
        else:
            db.add(Attendance(student_id=r.student_id, subject_id=r.subject_id, teacher_id=teacher.id, date=r.date, status=r.status))
    await db.commit()
    return api_response_success(message="Attendance saved")


async def get_marks(db, user):
    teacher = await _get_teacher(db, user)
    if not teacher:
        return api_response_error(message="Teacher profile not found", status_code=StatusCode.notFound)
    rows = (await db.execute(select(Marks).where(Marks.teacher_id == teacher.id))).scalars().all()
    return api_response_success(data=[{"id": m.id, "student_id": m.student_id, "exam_id": m.exam_id, "subject_id": m.subject_id, "marks_obtained": m.marks_obtained, "marks_total": m.marks_total} for m in rows])


async def add_marks(db, user, payload):
    teacher = await _get_teacher(db, user)
    if not teacher:
        return api_response_error(message="Teacher profile not found", status_code=StatusCode.notFound)
    m = Marks(student_id=payload.student_id, exam_id=payload.exam_id, subject_id=payload.subject_id, teacher_id=teacher.id, marks_obtained=payload.marks_obtained, marks_total=payload.marks_total)
    db.add(m)
    await db.commit()
    return api_response_success(data={"id": m.id}, message="Marks added", status_code=StatusCode.create)


async def list_materials(db, user):
    teacher = await _get_teacher(db, user)
    if not teacher:
        return api_response_error(message="Teacher profile not found", status_code=StatusCode.notFound)
    rows = (await db.execute(select(StudyMaterial).where(StudyMaterial.teacher_id == teacher.id).order_by(StudyMaterial.created_at.desc()))).scalars().all()
    return api_response_success(data=[{"id": m.id, "title": m.title, "subject_id": m.subject_id, "file_type": m.file_type, "file_url": m.file_url, "created_at": m.created_at} for m in rows])


async def add_material(db, user, payload):
    teacher = await _get_teacher(db, user)
    if not teacher:
        return api_response_error(message="Teacher profile not found", status_code=StatusCode.notFound)
    m = StudyMaterial(title=payload.title, subject_id=payload.subject_id, teacher_id=teacher.id, file_url=payload.file_url, file_type=payload.file_type, file_size=payload.file_size or 0)
    db.add(m)
    await db.commit()
    return api_response_success(data={"id": m.id}, message="Material added", status_code=StatusCode.create)


async def list_assignments(db, user):
    teacher = await _get_teacher(db, user)
    if not teacher:
        return api_response_error(message="Teacher profile not found", status_code=StatusCode.notFound)
    rows = (await db.execute(select(Assignment).where(Assignment.teacher_id == teacher.id).order_by(Assignment.created_at.desc()))).scalars().all()
    return api_response_success(data=[{"id": a.id, "title": a.title, "subject_id": a.subject_id, "section": a.section, "due_date": a.due_date, "created_at": a.created_at} for a in rows])


async def add_assignment(db, user, payload):
    teacher = await _get_teacher(db, user)
    if not teacher:
        return api_response_error(message="Teacher profile not found", status_code=StatusCode.notFound)
    a = Assignment(title=payload.title, description=payload.description, subject_id=payload.subject_id, teacher_id=teacher.id, section=payload.section, due_date=payload.due_date)
    db.add(a)
    await db.commit()
    return api_response_success(data={"id": a.id}, message="Assignment created", status_code=StatusCode.create)


async def get_leave(db, user):
    rows = (await db.execute(select(LeaveRequest).where(LeaveRequest.userid == user.userid).order_by(LeaveRequest.created_at.desc()))).scalars().all()
    return api_response_success(data=[{"id": l.id, "from_date": l.from_date, "to_date": l.to_date, "reason": l.reason, "status": l.status, "created_at": l.created_at} for l in rows])


async def apply_leave(db, user, payload):
    l = LeaveRequest(userid=user.userid, from_date=payload.from_date, to_date=payload.to_date, reason=payload.reason)
    db.add(l)
    await db.commit()
    return api_response_success(data={"id": l.id}, message="Leave applied", status_code=StatusCode.create)
