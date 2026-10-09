from pydantic import BaseModel, Field
from typing import Optional


class ContactSchema(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    message: str = Field(..., min_length=1)


class AdmissionApplySchema(BaseModel):
    applicant_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    phone: str = Field(..., min_length=5)
    course_id: Optional[int] = None