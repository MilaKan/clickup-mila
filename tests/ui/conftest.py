
import pytest
import allure
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD


@pytest.fixture(scope='session')
def browser():
    with allure.step("Инициализация Playwright"):
        playwright = sync_playwright().start()
    with allure.step("Запуск браузера Chromium"):
        browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    yield browser
    with allure.step("Закрытие браузера"):
        browser.close()
    with allure.step("Остановка Playwright"):
        playwright.stop()


@pytest.fixture(scope='session')
def logged_in_page(browser):
    with allure.step("Создание нового контекста браузера"):
        context = browser.new_context()
    with allure.step("Создание новой страницы"):
        page = context.new_page()
    with allure.step("Авторизация с учетными данными"):
        login_page = LoginPage(page)
        login_page.login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

    yield page
    with allure.step("Закрытие контекста браузера"):
        context.close()
