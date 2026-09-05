"""Datos iniciales de la base. Se puede ejecutar cuantas veces se quiera."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.database import Base, SessionLocal, engine
# from src.entities.plan import Plan

PLANES_SEMILLA = [
    {
        "nombre_plan": "Mensualidad Básica",
        "costo": 60000.00,
        "duracion_meses": 1
    },
    {
        "nombre_plan": "Anualidad VIP",
        "costo": 600000.00,
        "duracion_meses": 12
    },
]

def crear_tablas() -> None:
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
    crear_tablas()
    db = SessionLocal()
    try:
        # planes = _insertar_si_falta(db, Plan, "nombre_plan", PLANES_SEMILLA)
        planes = 0
    finally:
        db.close()

    print(f"Seeder terminado. Filas nuevas: {planes}")

if __name__ == "__main__":
    main()
