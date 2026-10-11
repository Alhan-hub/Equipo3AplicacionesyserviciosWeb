from uuid import uuid4


def test_listar_miembros(client):
    response = client.get("/miembros")
    assert response.status_code == 200
    assert response.json() == []


def test_obtener_miembro_por_id_exitoso(client):
    payload = {"nombre": "Daniel", "edad": 25, "email": "daniel@example.com"}
    created = client.post("/miembros", json=payload)
    miembro_id = created.json()["id"]

    response = client.get(f"/miembros/{miembro_id}")

    assert response.status_code == 200
    assert response.json()["nombre"] == "Daniel"
    assert response.json()["email"] == "daniel@example.com"


def test_crear_miembro_exitoso(client):
    payload = {"nombre": "Ana", "edad": 28, "email": "ana@example.com"}

    response = client.post("/miembros", json=payload)

    assert response.status_code == 201
    assert response.json()["nombre"] == "Ana"
    assert response.json()["edad"] == 28
    assert response.json()["email"] == "ana@example.com"


def test_actualizar_miembro_exitoso(client):
    payload = {"nombre": "Carlos", "edad": 30, "email": "carlos@example.com"}
    created = client.post("/miembros", json=payload)
    miembro_id = created.json()["id"]
    new_payload = {"nombre": "Carlos Updated", "edad": 31, "email": "carlos.nuevo@example.com"}

    response = client.put(f"/miembros/{miembro_id}", json=new_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Carlos Updated"
    assert data["edad"] == 31
    assert data["email"] == "carlos.nuevo@example.com"


def test_eliminar_miembro_exitoso(client):
    payload = {"nombre": "Brenda", "edad": 27, "email": "brenda@example.com"}
    created = client.post("/miembros", json=payload)
    miembro_id = created.json()["id"]

    response = client.delete(f"/miembros/{miembro_id}")

    assert response.status_code == 204
    assert client.get(f"/miembros/{miembro_id}").status_code == 404


def test_obtener_miembro_inexistente(client):
    response = client.get(f"/miembros/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Miembro no encontrado"


def test_crear_miembro_con_datos_invalidos(client):
    payload = {"nombre": "A", "edad": "diego", "email": "x"}

    response = client.post("/miembros", json=payload)

    assert response.status_code == 422


def test_actualizar_miembro_con_datos_invalidos(client):
    payload = {"nombre": "Marcos", "edad": 24, "email": "marcos@example.com"}
    created = client.post("/miembros", json=payload)
    miembro_id = created.json()["id"]
    invalid_payload = {"nombre": "M", "edad": 13, "email": "m"}

    response = client.put(f"/miembros/{miembro_id}", json=invalid_payload)

    assert response.status_code == 422


def test_crear_miembro_email_duplicado(client):
    payload = {"nombre": "Laura", "edad": 20, "email": "laura@example.com"}
    client.post("/miembros", json=payload)

    response = client.post("/miembros", json=payload)

    assert response.status_code == 400
    assert "Ya existe un miembro con el email" in response.json()["detail"]


def test_eliminar_miembro_inexistente(client):
    response = client.delete(f"/miembros/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Miembro no encontrado"
