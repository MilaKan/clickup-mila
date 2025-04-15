import allure
from pages.base_page import BasePage

@allure.feature("Board Page")
class BoardPage(BasePage):

    BOARD_BUTTON_SELECTOR = '[data-test="data-view-item__Board"]'
    COMPLETE_SELECTOR = "[data-test='board-header']"
    DELETE_TASK_SELECTOR = ".nav-menu-item__name >> text='Delete'"
    TASK_NAME = '.open-task-clickable-area.ng-star-inserted'

    def __init__(self, page):
        super().__init__(page)
        self._endpoint = 'login'

    @allure.step("Навигация на доску")
    def navigate_to_board(self):
        with allure.step("Переход на главную страницу доски"):
            self.navigate_to()
        with allure.step("Клик по кнопке 'Board'"):
            self.wait_for_selector_and_click(self.BOARD_BUTTON_SELECTOR)

    @staticmethod
    @allure.step("Получение селектора для опций задачи: {task_name}")
    def get_task_option_selector(task_name):
        return f'[data-test="board-task__ellipsis-menu__{task_name}"]'

    @allure.step("Ожидание, пока задача {task_name} станет видимой")
    def wait_for_task_visible(self, task_name: str, timeout=15000):
        with allure.step(f"Ожидание видимости задачи {task_name}"):
            selector = f"text='{task_name}'"
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    @allure.step("Удаление задачи {task_name}")
    def delete_task(self,task_name):
        with allure.step(f"Наведение на задачу {task_name}"):
            self.page.hover(self.TASK_NAME)
        with allure.step(f"Клик по кнопке меню для задачи {task_name}"):
            more_button_selector = f'[data-test="board-actions-menu__ellipsis__{task_name}"]'
            self.wait_for_selector_and_click(more_button_selector)
        with allure.step("Проверка видимости кнопки 'Delete'"):
            self.assert_element_is_visible(self.DELETE_TASK_SELECTOR)
        with allure.step("Клик по кнопке 'Delete'"):
            self.wait_for_selector_and_click(self.DELETE_TASK_SELECTOR)

        with allure.step(f"Проверка, что задача {task_name} исчезла"):
            task_selector = f'[data-test="board-task__name-link__{task_name}"]'
            self.assert_element_is_not_visible(task_selector)
