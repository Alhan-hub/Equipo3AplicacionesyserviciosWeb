from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.crud import miembro as repo
from src.database.database import get_db
from src.schemas.miembro import MiembroCreate, MiembroRead, MiembroUpdate

router = APIRouter(prefix="/miembros", tags=["Miembros"])

@router.get("", response_model=list[MiembroRead])
def listar_miembros(db: Session = Depends(get_db)):
    return repo.listar(db)

@router.get("/{miembro_id}", response_model=MiembroRead)
def obtener_miembro(miembro_id: UUID, db: Session = Depends(get_db)):
    miembro = repo.obtener_por_id(db, miembro_id)
    if miembro is None:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return miembro

@router.post(
    "",
    response_model=MiembroRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_miembro(datos: MiembroCreate, db: Session = Depends(get_db)):
    return repo.crear(db, datos)

@router.put("/{miembro_id}", response_model=MiembroRead)
def actualizar_miembro(
    miembro_id: UUID, datos: MiembroUpdate, db: Session = Depends(get_db)
):
    miembro = repo.obtener_por_id(db, miembro_id)
    if miembro is None:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return repo.actualizar(db, miembro, datos)

@router.delete("/{miembro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_miembro(miembro_id: UUID, db: Session = Depends(get_db)):
    miembro = repo.obtener_por_id(db, miembro_id)
    if miembro is None:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    repo.eliminar(db, miembro)
