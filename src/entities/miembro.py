from uuid import UUID, uuid4
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.database.database import Base

class Miembro(Base):
    __tablename__ = "miembros"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True
    )
