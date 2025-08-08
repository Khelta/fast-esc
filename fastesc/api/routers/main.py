from fastapi import APIRouter

from fastesc.api.routers.models.country_router import router as country_router

router = APIRouter()
router.include_router(country_router)
