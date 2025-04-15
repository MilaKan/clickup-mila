import allure
from playwright.sync_api import expect

class BasePage:
    __BASE_URL = 'https://app.clickup.com'
    def __init__(self, page):
        self.page=page
        self._endpoint = ''

    def _get_full_url(self):
        return f"{self.__BASE_URL}/{self._endpoint}"

    @allure.step("Переход по URL страницы")
    def navigate_to(self):
        full_url = self._get_full_url()
        self.page.goto(full_url)
        self.page.wait_for_load_state('load')
        expect(self.page).to_have_url(full_url)

    @allure.step("Клик по селектору: {selector}")
    def wait_for_selector_and_click(self, selector):
        with allure.step(f"Ожидание и клик по {selector}"):
            self.page.wait_for_selector(selector)
            self.page.click(selector)

    @allure.step("Заполнение поля: {selector} значением: {value}")
    def wait_for_selector_and_fill(self,selector , value):
        with allure.step(f"Заполнение поля {selector} значением {value}"):
            self.page.wait_for_selector(selector)
            self.page.fill(selector, value)

    @allure.step("Ввод текста с задержкой в {selector}")
    def wait_for_selector_and_type(self,selector ,value , delay):
        with allure.step(f"Ввод '{value}' с задержкой {delay} в {selector}"):
            self.page.wait_for_selector(selector)
            self.page.type(selector,value, delay=delay)

    @allure.step("Проверка, что элемент {selector} видим")
    def assert_element_is_visible(self, selector,timeout=10000):
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    @allure.step("Проверка наличия текста '{text}' на странице")
    def assert_text_present_on_page(self, text):
        expect(self.page.locator("body")).to_contain_text(text)

    @allure.step("Проверка, что элемент {selector} НЕ видим")
    def assert_element_is_not_visible(self,selector):
        expect(self.page.locator(selector)).not_to_be_visible()

    @allure.step("Проверка, что значение поля {selector} равно {expected_value}")
    def assert_input_value(self,selector ,expected_value):
        expect(self.page.locator(selector)).to_have_value(expected_value)

    @allure.step("Проверка, что элемент {selector} отключен")
    def assert_element_is_disabled(self,selector):
        expect(self.page.locator(selector)).to_be_disabled()