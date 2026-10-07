import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ID global temporal para pruebas de actualización y eliminación
miembro_id_test = None


# --- 1. POST: Crear ---
def test_crear_miembro_normal():
    global miembro_id_test
    # Email dinámico para evitar colisiones de 'unique' en la BD
    datos = {
        "nombre": "Test QA",
        "edad": 25,
        "email": f"test_{uuid.uuid4()}@gimnasio.com",
    }
    response = client.post("/miembros", json=datos)

    assert response.status_code == 201
    respuesta_json = response.json()
    assert respuesta_json["nombre"] == "Test QA"
    miembro_id_test = respuesta_json["id"]


def test_crear_miembro_error_incompleto():
    # Falta el email, debe retornar 422 Unprocessable Entity
    datos = {"nombre": "Test Incompleto", "edad": 25}
    response = client.post("/miembros", json=datos)
    assert response.status_code == 422


# --- 2. GET: Listar ---
def test_listar_miembros_normal():
    response = client.get("/miembros")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_listar_miembros_error_metodo():
    # Enviar un PATCH a una ruta que solo acepta GET/POST
    response = client.patch("/miembros")
    assert response.status_code == 405  # Method Not Allowed


# --- 3. GET: Obtener por ID ---
def test_obtener_miembro_normal():
    response = client.get(f"/miembros/{miembro_id_test}")
    assert response.status_code == 200
    assert response.json()["id"] == miembro_id_test


def test_obtener_miembro_error_no_existe():
    # UUID válido pero inexistente
    id_falso = "12345678-1234-5678-1234-567812345678"
    response = client.get(f"/miembros/{id_falso}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Miembro no encontrado"


# --- 4. PUT: Actualizar ---
def test_actualizar_miembro_normal():
    datos_actualizados = {
        "nombre": "Test QA Actualizado",
        "edad": 26,
        "email": f"update_{uuid.uuid4()}@gimnasio.com",
    }
    response = client.put(f"/miembros/{miembro_id_test}", json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Test QA Actualizado"


def test_actualizar_miembro_error_invalido():
    # Enviar un string en un campo que espera integer (edad)
    datos_error = {"nombre": "Test", "edad": "veinte", "email": "test@test.com"}
    response = client.put(f"/miembros/{miembro_id_test}", json=datos_error)
    assert response.status_code == 422


# --- 5. DELETE: Eliminar ---
def test_eliminar_miembro_normal():
    response = client.delete(f"/miembros/{miembro_id_test}")
    assert response.status_code == 204  # No Content


def test_eliminar_miembro_error_ya_eliminado():
    # Intentar eliminar el mismo registro que acaba de ser borrado
    response = client.delete(f"/miembros/{miembro_id_test}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Miembro no encontrado"
