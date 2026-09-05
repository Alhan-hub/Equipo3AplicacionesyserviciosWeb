from uuid import UUID
from pydantic import BaseModel, Field

class MiembroCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    edad: int = Field(ge=14, le=100)
    email: str = Field(min_length=5, max_length=254)

class MiembroUpdate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    edad: int = Field(ge=14, le=100)
    email: str = Field(min_length=5, max_length=254)

class MiembroRead(BaseModel):
    id: UUID
    nombre: str
    edad: int
    email: str

    model_config = {"from_attributes": True}
