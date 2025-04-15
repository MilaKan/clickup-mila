# tests/api/test_tasks.py
import pytest
from api_clients.task_api import TaskAPI
from utils.helpers import CLICKUP_API


def test_get_team(task_api, get_team_fixture):
    response = task_api.get_team()
    assert response.status_code == 200
    teams = response.json()['teams']
    assert len(teams) > 0
    assert teams is not None


def test_get_space(task_api, get_team_fixture, get_space_fixture):
    response = task_api.get_space(get_team_fixture['id'])
    assert response.status_code == 200
    spaces = response.json()['spaces']
    assert spaces is not None


def test_create_task(task_api, get_list_fixture, create_task_fixture):
    assert create_task_fixture['id'] is not None
    assert create_task_fixture['name'] == "Test Task"


def test_get_task(task_api,create_task_fixture):
    response = task_api.get_task(create_task_fixture['id'])  # Должен быть такой метод
    assert response.status_code == 200
    task = response.json()
    assert task['id'] == create_task_fixture['id']
    assert task['name'] == create_task_fixture['name']

def test_update_task(task_api,create_task_fixture):
    task_id = create_task_fixture["id"]
    update_data = {
        "name": "Updated Task Name",
        "description": "New Description"
    }
    response = task_api.update_task(task_id=task_id,task_update=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["name"] == update_data["name"]

def test_delete_task(task_api,create_task_fixture):
    response = task_api.delete_task(create_task_fixture['id'])
    assert response.status_code == 204, "Не удалось удалить задачу"
    post_delete_check = task_api.get_task(create_task_fixture['id'])
    assert post_delete_check.status_code == 404, "Задача все еще доступна после удаления"

#Негативный тест для Get Task
def test_unauthorized_access(create_task_fixture):
    invalid_api = TaskAPI(base_url=CLICKUP_API, api_key="invalid_key")
    response = invalid_api.get_task(create_task_fixture['id'])
    assert response.status_code == 401  # Unauthorized


#Негативный тест для Update Task
def test_update_task_negative(task_api,create_task_fixture):
    task_id = create_task_fixture["id"]
    response = task_api.update_task(task_id=task_id,task_update="invalid_text")
    assert response.status_code == 400


#Негативный тест для Delete Task
def test_delete_with_extra_params(task_api, create_task_fixture):
    response = task_api.session.delete(f"{task_api.base_url}/task/")
    assert response.status_code == 404, "Ожидалось негативный тест"


@pytest.mark.parametrize("task_data,expected_status,error_keyword", [
    ({}, 400, "required field"),
    ({"шшш": "Test name"}, 400, "empty"),
    ({"name": "Valid", "status": "invalid_status"}, 400, "invalid status"),
    ({"name": "Valid", "due_date": "2024-01-01"}, 400, "invalid date"),
    (None, 400, "invalid json"),
    ({"invalid_name":"name"}, 400, "invalid name")
])
def test_create_task_negative(task_api, get_list_fixture, task_data, expected_status, error_keyword):
    payload = task_data or {}
    if "list_id" not in payload or payload["list_id"] != "invalid_list_123":
        payload["list_id"] = get_list_fixture["id"]

    response = task_api.create_task(payload.pop("list_id", get_list_fixture["id"]), payload)
    assert response.status_code == expected_status, \
        f"Ожидался статус {expected_status}, получен {response.status_code}. Ответ: {response.text}"

