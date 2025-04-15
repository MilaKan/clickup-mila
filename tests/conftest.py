# tests/conftest.py
import pytest
from api_clients.task_api import TaskAPI
from utils.helpers import CLICKUP_API_KEY, CLICKUP_API


@pytest.fixture(scope="session")
def task_api():
    api = TaskAPI(CLICKUP_API, CLICKUP_API_KEY)

    # Проверка соединения
    response = api.get_team()
    if response.status_code != 200:
        pytest.fail(f"API connection failed: {response.status_code}")
    return api

@pytest.fixture
def get_team_fixture(task_api):
    response = task_api.get_team()
    return response.json()['teams'][0]


@pytest.fixture
def get_space_fixture(task_api, get_team_fixture):
    response = task_api.get_space(get_team_fixture['id'])
    return response.json()['spaces'][0]


@pytest.fixture
def get_folder_fixture(task_api, get_space_fixture):
    response = task_api.get_folder(get_space_fixture['id'])
    return response.json()['folders'][0]


@pytest.fixture
def get_list_fixture(task_api, get_folder_fixture):
    response = task_api.get_list(get_folder_fixture['id'])
    return response.json()['lists'][0]


@pytest.fixture
def create_task_fixture(task_api, get_list_fixture):
    task_data = {"name": "Test Task", "description": "Test"}
    response = task_api.create_task(get_list_fixture['id'], task_data)
    task = response.json()
    yield task

    task_api.delete_task(task['id'])

