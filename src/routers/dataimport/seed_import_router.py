from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.database import get_session
from src.seed import seed_database

router = APIRouter(prefix="/data_import", tags=["import"])


@router.get("/songs/", response_model=str)
def seed_init_database(*, session: Session = Depends(get_session)):
    seed_database(session)
    return "Seeding complete"
