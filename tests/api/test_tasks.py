# tests/api/test_tasks.py
def test_get_team(task_api, test_team):
    response = task_api.get_team()
    assert response.status_code == 200
    teams = response.json()['teams']
    assert len(teams) > 0
    assert teams is not None


def test_get_space(task_api, test_team, test_space):
    response = task_api.get_space(test_team['id'])
    assert response.status_code == 200
    spaces = response.json()['spaces']
    assert spaces is not None


def test_create_task(task_api, get_list, create_task):
    print(f"Используемый API ключ: {task_api.session.headers['Authorization']}")
    assert create_task['id'] is not None
    assert create_task['name'] == "Test Task"

    response = task_api.get_list(get_list['id'])
    assert response.status_code == 200, "Ошибка при создании задачи"
    tasks = response.json()
    assert tasks is not None

def test_get_task(task_api,test_list,test_task):
    response = task_api.get_task(test_task['id'])  # Должен быть такой метод
    assert response.status_code == 200
    task = response.json()
    assert task['id'] == test_task['id']
    assert task['name'] == test_task['name']

def test_update_task(task_api,test_list,test_task):
    response = task_api.update_task(test_task['id'])
    assert response.status_code == 200
    task = response.json()
    assert task['id'] == test_task['id']
    assert task['name'] == test_task['name']

def test_delete_task(task_api,test_list,test_task):
    response = task_api.delete_task(test_task['id'])
    assert response.status_code == 200, "Не удалось удалить задачу"

def test_check_delete(task_api,test_list,test_task):
    response = task_api.get_task(test_task['id'])
    assert response.status_code == 404, "Задача все еще существует после удаления"


