from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import String, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class Plan(Base):
    __tablename__ = "planes"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    nombre_plan: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    costo: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    duracion_meses: Mapped[int] = mapped_column(Integer, nullable=False)
