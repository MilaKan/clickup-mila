
from pages.board_page import BoardPage



def test_task_delete(logged_in_page, create_task_fixture, task_api):
    task_id = create_task_fixture['id']
    task_name = create_task_fixture['name']
    print(f"Task ID: {task_id}, Task Name: {task_name}")
    board_page = BoardPage(logged_in_page)
    board_page.navigate_to_board()
    board_page.wait_for_task_visible(task_name)
    board_page.delete_task(task_name)
    response = task_api.get_task(task_id)
    assert response.status_code == 404, "Задача не была удалена"

