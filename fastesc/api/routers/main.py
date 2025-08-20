from fastapi import APIRouter

from fastesc.api.routers.dataimport.contest_import_router import router as contest_import_router
from fastesc.api.routers.dataimport.country_import_router import router as country_import_router
from fastesc.api.routers.dataimport.seed_import_router import router as seed_import_router
from fastesc.api.routers.dataimport.song_import_router import router as song_import_router
from fastesc.api.routers.models.contest_router import router as contest_router
from fastesc.api.routers.models.country_router import router as country_router

router = APIRouter()
router.include_router(country_router)
router.include_router(country_import_router)
router.include_router(contest_import_router)
router.include_router(contest_router)
router.include_router(seed_import_router)
router.include_router(song_import_router)
