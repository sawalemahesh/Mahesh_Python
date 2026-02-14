from selenium.webdriver.common.by import By
from POM.utilities.common_methods import CommonMethods


class LoginPage:

    # Locators
    username_input = (By.ID, "user-name")
    password_input = (By.ID, "password")
    login_button = (By.ID, "login-button")
    error_message = (By.XPATH, "//h3[@data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.common = CommonMethods(driver)

    # Page Actions
    def enter_username(self, username):
        self.common.send_text(self.username_input, username)

    def enter_password(self, password):
        self.common.send_text(self.password_input, password)

    def click_login(self):
        self.common.click(self.login_button)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        return self.common.get_text(self.error_message)
