
import allure
import pytest
from api_clients.task_api import TaskAPI
from utils.helpers import CLICKUP_API


@allure.feature("Команды")
@allure.description("Проверка получения списка команд через API.")
def test_get_team(task_api, get_team_fixture):
    with allure.step("Отправка запроса на получение списка команд"):
        response = task_api.get_team()
    with allure.step("Проверка корректности ответа"):
        assert response.status_code == 200
        teams = response.json()['teams']
        assert len(teams) > 0
        assert teams is not None


@allure.feature("Пространства")
@allure.description("Проверка получения пространств по команде через API.")
def test_get_space(task_api, get_team_fixture, get_space_fixture):
    with allure.step(f"Получение пространств для команды ID {get_team_fixture['id']}"):
        response = task_api.get_space(get_team_fixture['id'])
    with allure.step("Проверка ответа"):
        assert response.status_code == 200
        spaces = response.json()['spaces']
        assert spaces is not None


@allure.feature("Задачи")
@allure.description("Создание новой задачи через API и проверка возвращаемого ID и имени.")
def test_create_task(task_api, get_list_fixture, create_task_fixture):
    with allure.step("Проверка, что задача успешно создана"):
        assert create_task_fixture['id'] is not None
        assert create_task_fixture['name'] == "Test Task"


@allure.feature("Задачи")
@allure.description("Получение ранее созданной задачи по ID через API.")
def test_get_task(task_api, create_task_fixture):
    with allure.step("Запрос задачи по ID"):
        response = task_api.get_task(create_task_fixture['id'])
    with allure.step("Проверка полученных данных задачи"):
        assert response.status_code == 200
        task = response.json()
        assert task['id'] == create_task_fixture['id']
        assert task['name'] == create_task_fixture['name']


@allure.feature("Задачи")
@allure.description("Обновление задачи и проверка изменений.")
def test_update_task(task_api, create_task_fixture):
    task_id = create_task_fixture["id"]
    update_data = {
        "name": "Updated Task Name",
        "description": "New Description"
    }
    with allure.step(f"Обновление задачи {task_id}"):
        response = task_api.update_task(task_id=task_id, task_update=update_data)
    with allure.step("Проверка обновлённой задачи"):
        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["name"] == update_data["name"]


@allure.feature("Задачи")
@allure.description("Удаление задачи и проверка, что она недоступна.")
def test_delete_task(task_api, create_task_fixture):
    with allure.step("Удаление задачи по ID"):
        response = task_api.delete_task(create_task_fixture['id'])
        assert response.status_code == 204, "Не удалось удалить задачу"
    with allure.step("Проверка, что задача удалена и возвращает 404"):
        post_delete_check = task_api.get_task(create_task_fixture['id'])
        assert post_delete_check.status_code == 404, "Задача все еще доступна после удаления"


@allure.feature("Авторизация")
@allure.description("Проверка отказа в доступе при использовании недействительного API ключа.")
def test_unauthorized_access(create_task_fixture):
    with allure.step("Создание клиента с недействительным API ключом"):
        invalid_api = TaskAPI(base_url=CLICKUP_API, api_key="invalid_key")
    with allure.step("Попытка получить задачу"):
        response = invalid_api.get_task(create_task_fixture['id'])
        assert response.status_code == 401  # Unauthorized


@allure.feature("Задачи")
@allure.description("Негативный тест: передача некорректных данных при обновлении задачи.")
def test_update_task_negative(task_api, create_task_fixture):
    with allure.step("Попытка обновления задачи с некорректными данными"):
        task_id = create_task_fixture["id"]
        response = task_api.update_task(task_id=task_id, task_update="invalid_text")
        assert response.status_code == 400


@allure.feature("Задачи")
@allure.description("Негативный тест: удаление задачи без указания ID.")
def test_delete_task_negative(task_api):
    invalid_task_id = "invalid_id_12345"
    with allure.step(f"Попытка удалить задачу с некорректным ID: {invalid_task_id}"):
        response = task_api.delete_task(invalid_task_id)
        assert response.status_code == 401, "Ожидалось негативный тест"


@allure.feature("Задачи")
@allure.description("Негативные тесты создания задач с некорректными данными.")
@pytest.mark.parametrize("task_data,expected_status,error_keyword", [
    ({}, 400, "required field"),
    ({"шшш": "Test name"}, 400, "empty"),
    ({"name": "Valid", "status": "invalid_status"}, 400, "invalid status"),
    ({"name": "Valid", "due_date": "2024-01-01"}, 400, "invalid date"),
    (None, 400, "invalid json"),
    ({"invalid_name": "name"}, 400, "invalid name")
])
def test_create_task_negative(task_api, get_list_fixture, task_data, expected_status, error_keyword):
    with allure.step("Подготовка тела запроса"):
        payload = task_data or {}
        if "list_id" not in payload or payload["list_id"] != "invalid_list_123":
            payload["list_id"] = get_list_fixture["id"]

    with allure.step(f"Отправка запроса на создание задачи с данными: {payload}"):
        response = task_api.create_task(payload.pop("list_id", get_list_fixture["id"]), payload)
    with allure.step("Проверка ожидаемого кода ошибки"):
        assert response.status_code == expected_status, \
            f"Ожидался статус {expected_status}, получен {response.status_code}. Ответ: {response.text}"
