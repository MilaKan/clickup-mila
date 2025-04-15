import self

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = 'login'

    USERNAME_SELECTOR = '#login-email-input'
    PASSWORD_SELECTOR = '#login-password-input'
    LOGIN_BUTTON_SELECTOR = '[data-test="login-submit"]'
    PASSWORD_INVALID_SELECTOR = '#login-password-input'
    CONTINUE_SELECTOR = "text='Continue on web anyway'"

    def login(self, username, password):
        self.navigate_to()
        self.assert_text_present_on_page('Welcome back!')
        self.wait_for_selector_and_type(self.USERNAME_SELECTOR, username, 100)
        self.wait_for_selector_and_fill(self.PASSWORD_SELECTOR, password)
        self.assert_input_value(self.USERNAME_SELECTOR, username)
        self.assert_input_value(self.PASSWORD_SELECTOR,password)
        with self.page.expect_navigation(timeout=15000):
            self.wait_for_selector_and_click(self.LOGIN_BUTTON_SELECTOR)
        if self.page.is_visible(self.CONTINUE_SELECTOR, timeout=5000):
            self.page.click(self.CONTINUE_SELECTOR)
        self.assert_text_present_on_page('Board')

    def login_negative(self, username, password_invalid):
        self.navigate_to()
        self.wait_for_selector_and_type(self.USERNAME_SELECTOR, username,100)
        self.wait_for_selector_and_fill(self.PASSWORD_INVALID_SELECTOR, password_invalid)
        self.assert_element_is_disabled(self.LOGIN_BUTTON_SELECTOR)




