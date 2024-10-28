"""
Casos de prueba para el servicio web de contador
"""
import pytest
from counter import app
from http import HTTPStatus

@pytest.fixture
def client():
    # Configuración del cliente de prueba de Flask
    return app.test_client()

def test_create_a_counter(client):
    """Debe crear un contador"""
    result = client.post("/counters/test_counter")
    assert result.status_code == HTTPStatus.CREATED
    data = result.get_json()
    assert "test_counter" in data
    assert data["test_counter"] == 0

def test_duplicate_counter(client):
    """Debe devolver un error para duplicados"""
    result = client.post("/counters/test_counter")
    assert result.status_code == HTTPStatus.CREATED
    result = client.post("/counters/test_counter")
    assert result.status_code == HTTPStatus.CONFLICT
