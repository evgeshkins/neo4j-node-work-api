import pytest
from fastapi.testclient import TestClient
from main import app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = TestClient(app)

@pytest.fixture
def auth_header():
    """Возвращает заголовок авторизации для тестирования."""
    return {
        "Authorization": "Bearer secret-token"
    }

def test_get_all_nodes():
    response = client.get("/nodes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_node_and_relations():
    """Тест на получение узла и всех его связей."""
    # Перед тестом убедитесь, что узел с ID 1 существует
    node_id = 1
    response = client.get(f"/nodes/{node_id}")
    assert response.status_code == 200
    data = response.json()
    logger.info(data)

def test_insert_node_and_relationships(auth_header):
    """Тест на добавление узла и связей."""
    test_data = {
        "node": {
            "node_id": 34444,
            "label": "User",
            "name": "Жорик Мажорик",
            "screen_name": "jmurik",
            "sex": 2,
            "home_town": "San Francisco"
        },
        "relationships": [
            {
                "id": 34444,
                "type": "Follow",
                "end_node_id": 2548
            }
        ]
    }

    # Используем TestClient для отправки запроса
    client = TestClient(app)
    response = client.post("/graph/insert", json=test_data, headers=auth_header)

    # Проверяем, что статус код 200 (OK)
    assert response.status_code == 200

    # Проверяем, что возвращается правильный ответ
    assert response.json() == {"status": "Узел и связи добавлены.", "response": "Узел и связи добавлены."}

def test_delete_node_and_relationships(auth_header):
    node_id = 34464
    response = client.delete(f"/nodes/{node_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json() == {"status": "Узел удален.", "response": "Узел удален."}