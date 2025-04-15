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

