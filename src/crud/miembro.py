from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.entities.miembro import Miembro
from src.schemas.miembro import MiembroCreate, MiembroUpdate

def listar(db: Session) -> list[Miembro]:
    return list(db.scalars(select(Miembro).order_by(Miembro.nombre)))

def obtener_por_id(db: Session, miembro_id: UUID) -> Miembro | None:
    return db.get(Miembro, miembro_id)

def crear(db: Session, datos: MiembroCreate) -> Miembro:
    miembro = Miembro(
        nombre=datos.nombre,
        edad=datos.edad,
        email=datos.email,
    )
    db.add(miembro)
    db.commit()
    db.refresh(miembro)
    return miembro

def actualizar(db: Session, miembro: Miembro, datos: MiembroUpdate) -> Miembro:
    miembro.nombre = datos.nombre
    miembro.edad = datos.edad
    miembro.email = datos.email
    db.commit()
    db.refresh(miembro)
    return miembro

def eliminar(db: Session, miembro: Miembro) -> None:
    db.delete(miembro)
    db.commit()
    db.commit()
