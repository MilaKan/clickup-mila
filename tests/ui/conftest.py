import pytest
from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage


@pytest.fixture(scope = 'session')
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless = False, slow_mo=1000)
    yield browser
    browser.close()
    playwright.stop()

@pytest.fixture(scope='session')
def logged_in_page(browser):
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.login('milanakan2001@gmail.com', 'Milakan2307')

    yield page
    context.close()