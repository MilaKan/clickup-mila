
import allure
from pages.board_page import BoardPage


@allure.feature("Удаление задачи")
@allure.description("Удаление задачи через UI и проверка её удаления через API.")
def test_task_delete(logged_in_page, create_task_fixture, task_api):
    task_id = create_task_fixture['id']
    task_name = create_task_fixture['name']
    board_page = BoardPage(logged_in_page)
    with allure.step("Переход на доску и ожидание появления задачи"):
        board_page.navigate_to_board()
    board_page.wait_for_task_visible(task_name)
    with allure.step(f"Удаление задачи с именем {task_name}"):
        board_page.delete_task(task_name)
    with allure.step(f"Проверка статуса удаления задачи с ID {task_id} через API"):
        response = task_api.get_task(task_id)
        assert response.status_code == 404, "Задача не была удалена"


@allure.description("Создание задачи через UI, проверка её наличия через API и удаление через API")
def test_create_task_ui(logged_in_page, task_api, get_list_fixture):
    board_page = BoardPage(logged_in_page)
    task_name = "UI Created Task"
    with allure.step("Создание задачи через UI"):
        board_page.create_task_ui(task_name)
    with allure.step("Получение списка задач через API"):
        list_id = get_list_fixture['id']
        response = task_api.session.get(f"{task_api.base_url}/list/{list_id}/task")
        assert response.status_code == 200, "Не удалось получить список задач через API"
    with allure.step("Поиск созданной задачи по имени"):
        tasks = response.json()['tasks']
        created_task = next((task for task in tasks if task['name'] == task_name), None)
        assert created_task is not None, "Созданная задача не найдена через API"
        task_id = created_task['id']
    with allure.step(f"Удаление задачи '{task_name}' через API по ID {task_id}"):
        delete_response = task_api.delete_task(task_id)
        assert delete_response.status_code == 204, "Не удалось удалить задачу через API"
    with allure.step("Проверка, что задача больше не существует"):
        check_response = task_api.get_task(task_id)
        assert check_response.status_code == 404, "Задача всё ещё существует после удаления"
