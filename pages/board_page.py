from pages.base_page import BasePage

class BoardPage(BasePage):

    BOARD_BUTTON_SELECTOR = '[data-test="data-view-item__Board"]'
    COMPLETE_SELECTOR = "[data-test='board-header']"
    DELETE_TASK_SELECTOR = ".nav-menu-item__name >> text='Delete'"
    TASK_NAME = '.open-task-clickable-area.ng-star-inserted'

    def __init__(self, page):
        super().__init__(page)
        self._endpoint = 'login'

    def navigate_to_board(self):
        self.navigate_to()
        self.wait_for_selector_and_click(self.BOARD_BUTTON_SELECTOR)

    @staticmethod
    def get_task_option_selector(task_name):
        return f'[data-test="board-task__ellipsis-menu__{task_name}"]'

    def wait_for_task_visible(self, task_name: str, timeout=15000):
        selector = f"text='{task_name}'"
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def delete_task(self,task_name):
        self.page.hover(self.TASK_NAME)
        more_button_selector = f'[data-test="board-actions-menu__ellipsis__{task_name}"]'
        self.wait_for_selector_and_click(more_button_selector)
        self.assert_element_is_visible(self.DELETE_TASK_SELECTOR)
        self.wait_for_selector_and_click(self.DELETE_TASK_SELECTOR)

        task_selector = f'[data-test="board-task__name-link__{task_name}"]'
        self.assert_element_is_not_visible(task_selector)
