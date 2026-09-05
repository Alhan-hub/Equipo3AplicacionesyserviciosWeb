from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class PlanCreate(BaseModel):
    nombre_plan: str = Field(min_length=2, max_length=100)
    costo: Decimal = Field(gt=0, description="El costo debe ser mayor a 0")
    duracion_meses: int = Field(gt=0, le=120)


class PlanUpdate(BaseModel):
    nombre_plan: str = Field(min_length=2, max_length=100)
    costo: Decimal = Field(gt=0)
    duracion_meses: int = Field(gt=0, le=120)


class PlanRead(BaseModel):
    id: UUID
    nombre_plan: str
    costo: Decimal
    duracion_meses: int
    model_config = {"from_attributes": True}
