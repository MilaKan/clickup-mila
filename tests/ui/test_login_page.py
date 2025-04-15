import allure
from pages.login_page import LoginPage

@allure.feature("Авторизация")
@allure.description("Проверка успешной авторизации и наличия элемента 'Board' после входа.")
def test_login(browser, logged_in_page):
    with allure.step("Проверка успешной авторизации"):
        assert 'Board' in logged_in_page.content()

@allure.feature("Авторизация")
@allure.description("Проверка успешной авторизации и наличия элемента 'Board' после входа.")
def test_login_negative(browser):
    with allure.step("Открытие страницы входа и попытка авторизации с некорректными данными"):
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.login_negative('milanakan2001@gmail.com','12345')
