from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_obtener_pedido_inexistente_devuelve_404():
    response = client.get("/orders/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "No existe"


def test_confirmar_pedido_y_rechazar_confirmacion_duplicada():
    first_response = client.post("/orders/O013/confirm")
    assert first_response.status_code == 200
    assert first_response.json()["status"] == "CONFIRMED"

    second_response = client.post("/orders/O013/confirm")
    assert second_response.status_code == 409


def test_confirmar_pedido_vacio_devuelve_422():
    response = client.post("/orders/O007/confirm")
    assert response.status_code == 422
