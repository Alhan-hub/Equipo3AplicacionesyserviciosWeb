from uuid import uuid4


def test_listar_planes(client):
    response = client.get("/planes")
    assert response.status_code == 200
    assert response.json() == []


def test_obtener_plan_por_id_exitoso(client):
    payload = {"nombre_plan": "Plan Básico", "costo": 120000.0, "duracion_meses": 1}
    created = client.post("/planes", json=payload)
    plan_id = created.json()["id"]

    response = client.get(f"/planes/{plan_id}")

    assert response.status_code == 200
    assert response.json()["nombre_plan"] == "Plan Básico"
    assert response.json()["costo"] == "120000.00"


def test_crear_plan_exitoso(client):
    payload = {"nombre_plan": "Plan Premium", "costo": 250000.0, "duracion_meses": 6}

    response = client.post("/planes", json=payload)

    assert response.status_code == 201
    assert response.json()["nombre_plan"] == "Plan Premium"
    assert response.json()["duracion_meses"] == 6


def test_actualizar_plan_exitoso(client):
    payload = {"nombre_plan": "Plan Gold", "costo": 180000.0, "duracion_meses": 3}
    created = client.post("/planes", json=payload)
    plan_id = created.json()["id"]
    update_payload = {"nombre_plan": "Plan Gold Plus", "costo": 220000.0, "duracion_meses": 4}

    response = client.put(f"/planes/{plan_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nombre_plan"] == "Plan Gold Plus"
    assert data["costo"] == "220000.00"
    assert data["duracion_meses"] == 4


def test_eliminar_plan_exitoso(client):
    payload = {"nombre_plan": "Plan Estudiante", "costo": 50000.0, "duracion_meses": 2}
    created = client.post("/planes", json=payload)
    plan_id = created.json()["id"]

    response = client.delete(f"/planes/{plan_id}")

    assert response.status_code == 204
    assert client.get(f"/planes/{plan_id}").status_code == 404


def test_obtener_plan_inexistente(client):
    response = client.get(f"/planes/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Plan no encontrado"


def test_crear_plan_con_datos_invalidos(client):
    payload = {"nombre_plan": "A", "costo": 0, "duracion_meses": 0}

    response = client.post("/planes", json=payload)

    assert response.status_code == 422


def test_actualizar_plan_con_datos_invalidos(client):
    payload = {"nombre_plan": "Plan Starter", "costo": 99000.0, "duracion_meses": 2}
    created = client.post("/planes", json=payload)
    plan_id = created.json()["id"]
    invalid_payload = {"nombre_plan": "A", "costo": -10, "duracion_meses": 0}

    response = client.put(f"/planes/{plan_id}", json=invalid_payload)

    assert response.status_code == 422


def test_crear_plan_con_nombre_duplicado(client):
    payload = {"nombre_plan": "Plan Familiar", "costo": 150000.0, "duracion_meses": 5}
    client.post("/planes", json=payload)

    response = client.post("/planes", json=payload)

    assert response.status_code == 400
    assert "Ya existe un plan con el nombre" in response.json()["detail"]


def test_eliminar_plan_inexistente(client):
    response = client.delete(f"/planes/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Plan no encontrado"
