from fastapi import APIRouter, Depends
from sqlmodel import Session

from fastesc.database import get_session
from fastesc.seed import seed_database

router = APIRouter(prefix="/data_import", tags=["import"])


@router.get("/seed_init/", response_model=str)
def seed_init_database(*, session: Session = Depends(get_session)):
    seed_database(session)
    return "Seeding complete"
