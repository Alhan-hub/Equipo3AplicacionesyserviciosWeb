from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database.database import Base, engine

from src.api.plan import router as planes_router

# Cuando los integrantes terminen, descomentarán sus routers aquí:
# from src.api.miembro import router as miembros_router
# from src.api.entrenador import router as entrenadores_router

from src.entities import plan as _plan_model

# from src.entities import miembro as _miembro_model
# from src.entities import entrenador as _entrenador_model


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Gimnasio - Examen 1",
    description="API REST con FastAPI, SQLAlchemy y Neon PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["General"])
def inicio():
    return {
        "mensaje": "API de Gestión de Gimnasio - Activa",
        "docs": "/docs",
    }


app.include_router(planes_router)
# app.include_router(miembros_router)
# app.include_router(entrenadores_router)
