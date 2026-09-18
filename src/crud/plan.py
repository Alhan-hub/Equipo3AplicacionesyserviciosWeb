from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.plan import Plan
from src.schemas.plan import PlanCreate, PlanUpdate


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
