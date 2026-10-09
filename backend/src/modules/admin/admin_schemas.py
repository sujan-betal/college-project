from typing import Optional
from datetime import date as date_type
from pydantic import BaseModel, Field, EmailStr


class CreateUserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: Optional[EmailStr] = None
    role: str = Field(default="STUDENT")
    status: str = Field(default="ACTIVE")
    designation: Optional[str] = None
    department_id: Optional[int] = None
    permissions: Optional[list[str]] = None
    role_template: Optional[str] = None


class SetPermissionsSchema(BaseModel):
    permissions: list[str] = Field(default_factory=list)


class UpdateUserStatusSchema(BaseModel):
    status: str = Field(..., min_length=1)


class DepartmentCreateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    description: Optional[str] = None


class CourseCreateSchema(BaseModel):
    department_id: int
    name: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    duration_years: int = 3
    total_seats: int = 60
    annual_fee: float = 0


class FeeStructureCreateSchema(BaseModel):
    course_id: int
    head: str = Field(..., min_length=1)
    amount: float = 0
    due_date: Optional[date_type] = None


class ExamCreateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    course_id: Optional[int] = None
    semester: Optional[int] = None
    start_date: Optional[date_type] = None
    is_published: int = 0


class StatusUpdateSchema(BaseModel):
    status: str = Field(..., min_length=1)