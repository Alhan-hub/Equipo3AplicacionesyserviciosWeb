from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.crud import plan as repo
from src.database.database import get_db
from src.schemas.plan import PlanCreate, PlanRead, PlanUpdate

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
        raise HTTPException(status_code=400, detail=str(e)) from e


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
