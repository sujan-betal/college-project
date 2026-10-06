from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.common_schema import api_response_success

router = APIRouter(prefix="/api/public", tags=["Public"])


@router.get("/home")
async def public_home():
    return api_response_success(
        data={
            "college_name": "AstraVidya Institute of Technology",
            "slogan": "Ignite. Innovate. Excel.",
            "stats": {"students": 4200, "programs": 38, "faculty": 220, "established": 1998}
        }
    )


@router.get("/notices")
async def public_notices():
    return api_response_success(data=[])


@router.get("/courses")
async def public_courses():
    return api_response_success(data=[])


@router.get("/events")
async def public_events():
    return api_response_success(data=[])


@router.get("/gallery")
async def public_gallery():
    return api_response_success(data=[])