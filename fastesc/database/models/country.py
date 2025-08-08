from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from fastesc.database.models.base import Base


class Country(Base):
    __tablename__ = 'country'

    name: Mapped[str] = mapped_column("name", nullable=False)
    alpha2: Mapped[str] = mapped_column("alpha2", String(length=2), nullable=False)
