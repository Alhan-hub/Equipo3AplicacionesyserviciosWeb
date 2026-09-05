from decimal import Decimal
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from sqlalchemy import String, Numeric, Integer, select
from sqlalchemy.orm import Mapped, mapped_column, Session
from src.database.database import Base, get_db
from src.entities.plan import Plan
from src.crud import plan as repo
from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.plan import PlanCreate, PlanRead, PlanUpdate


class Plan(Base):
    _tablename_ = "planes"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    nombre_plan: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    costo: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    duracion_meses: Mapped[int] = mapped_column(Integer, nullable=False)


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


def listar(db: Session) -> list[Plan]:
    return list(db.scalars(select(Plan).order_by(Plan.nombre_plan)))


def obtener_por_id(db: Session, plan_id: UUID) -> Plan | None:
    return db.get(Plan, plan_id)


def crear(db: Session, datos: PlanCreate) -> Plan:
    existe = db.scalar(select(Plan).where(Plan.nombre_plan == datos.nombre_plan))
    if existe:
        raise ValueError(f"Ya existe un plan con el nombre '{datos.nombre_plan}'")

    plan = Plan(
        nombre_plan=datos.nombre_plan,
        costo=datos.costo,
        duracion_meses=datos.duracion_meses,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def actualizar(db: Session, plan: Plan, datos: PlanUpdate) -> Plan:
    plan.nombre_plan = datos.nombre_plan
    plan.costo = datos.costo
    plan.duracion_meses = datos.duracion_meses
    db.commit()
    db.refresh(plan)
    return plan


def eliminar(db: Session, plan: Plan) -> None:
    db.delete(plan)
    db.commit()


router = APIRouter(prefix="/planes", tags=["Planes"])


@router.get("", response_model=list[PlanRead])
def listar_planes(db: Session = Depends(get_db)):
    return repo.listar(db)


@router.get("/{plan_id}", response_model=PlanRead)
def obtener_plan(plan_id: UUID, db: Session = Depends(get_db)):
    plan = repo.obtener_por_id(db, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return plan


@router.post("", response_model=PlanRead, status_code=status.HTTP_201_CREATED)
def crear_plan(datos: PlanCreate, db: Session = Depends(get_db)):
    try:
        return repo.crear(db, datos)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{plan_id}", response_model=PlanRead)
def actualizar_plan(plan_id: UUID, datos: PlanUpdate, db: Session = Depends(get_db)):
    plan = repo.obtener_por_id(db, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return repo.actualizar(db, plan, datos)


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_plan(plan_id: UUID, db: Session = Depends(get_db)):
    plan = repo.obtener_por_id(db, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    repo.eliminar(db, plan)
