from pages.login_page import LoginPage

def test_login(browser, logged_in_page):
    assert 'Board' in logged_in_page.content()

def test_login_negative(browser):
    page = browser.new_page()
    login_page = LoginPage(page)
    login_page.login_negative('milanakan2001@gmail.com','12345')
