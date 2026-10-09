from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.modules.public import public_services
from src.modules.public.public_schemas import AdmissionApplySchema, ContactSchema

router = APIRouter(prefix="/api/public", tags=["Public"])


@router.get("/home")
async def home(db: AsyncSession = Depends(get_db)):
    return await public_services.get_home(db)


@router.get("/site-content")
async def site_content(db: AsyncSession = Depends(get_db)):
    return await public_services.get_site_content(db)


@router.get("/notices")
async def notices(db: AsyncSession = Depends(get_db)):
    return await public_services.get_notices(db)


@router.get("/courses")
async def courses(db: AsyncSession = Depends(get_db)):
    return await public_services.get_courses(db)


@router.get("/departments")
async def departments(db: AsyncSession = Depends(get_db)):
    return await public_services.get_departments(db)


@router.get("/faculty")
async def faculty(db: AsyncSession = Depends(get_db)):
    return await public_services.get_faculty(db)


@router.get("/events")
async def events(db: AsyncSession = Depends(get_db)):
    return await public_services.get_events(db)


@router.get("/gallery")
async def gallery(db: AsyncSession = Depends(get_db)):
    return await public_services.get_gallery(db)


@router.post("/admissions")
async def apply(payload: AdmissionApplySchema, db: AsyncSession = Depends(get_db)):
    return await public_services.apply_admission(db, payload)


@router.post("/contact")
async def contact(payload: ContactSchema, db: AsyncSession = Depends(get_db)):
    return await public_services.send_contact_message(db, payload)