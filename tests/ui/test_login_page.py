
import allure
from pages.login_page import LoginPage
from utils.helpers import CLICKUP_EMAIL


@allure.feature("Авторизация")
@allure.description("Проверка успешной авторизации и наличия элемента 'Board' после входа.")
def test_login(browser, logged_in_page):
    with allure.step("Проверка успешной авторизации"):
        assert 'Board' in logged_in_page.content()


@allure.feature("Авторизация")
@allure.description("Проверка невозможности авторизации с некорректными данными (негативный тест).")
def test_login_negative(browser):
    with allure.step("Открытие страницы входа и попытка авторизации с некорректными данными"):
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.login_negative(CLICKUP_EMAIL, '12345')
    with allure.step("Проверка, что кнопка входа неактивна при некорректных данных"):
        assert page.locator(login_page.LOGIN_BUTTON_SELECTOR).is_disabled(), "Ожидалось, что кнопка будет неактивна"
    with allure.step("Проверка, что вход не выполнен"):
        assert not page.locator("text='Board'").is_visible(timeout=3000), "Неожиданно выполнен вход при неверных данных"
