"""Datos iniciales de la base. Se puede ejecutar cuantas veces se quiera."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.database import Base, SessionLocal, engine
from src.entities.miembro import Miembro

MIEMBROS_SEMILLA = [
    {"nombre": "Alhan Rendon", "edad": 20, "email": "alhan@gimnasio.com"},
    {"nombre": "Richard Rendon", "edad": 40, "email": "richard@gimnasio.com"},
]


def crear_tablas() -> None:
    """Crea las tablas en la base de datos."""
    Base.metadata.create_all(bind=engine)
    print("Tablas verificadas/creadas.")


def _insertar_si_falta(
    db: Session,
    modelo: type,
    campo: str,
    filas: list[dict],
) -> int:
    insertadas = 0
    columna = getattr(modelo, campo)

    for datos in filas:
        etiqueta = datos[campo]
        existe = db.scalar(select(modelo).where(columna == etiqueta))
        if existe is not None:
            print(f"Ya existe: {etiqueta}")
            continue

        db.add(modelo(**datos))
        insertadas += 1
        print(f"Insertada: {etiqueta}")

    db.commit()
    return insertadas


def main() -> None:
    """Ejecuta el seeder."""
    crear_tablas()
    db = SessionLocal()
    try:
        miembros = _insertar_si_falta(db, Miembro, "email", MIEMBROS_SEMILLA)
    finally:
        db.close()

    print(f"Seeder terminado. Filas nuevas: {miembros}")


if __name__ == "__main__":
    main()
