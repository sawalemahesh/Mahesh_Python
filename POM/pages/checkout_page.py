from selenium.webdriver.common.by import By
from POM.utilities import common_methods as CommonMethods


class CheckoutPage:

    first_name_input = (By.ID, "first-name")
    last_name_input = (By.ID, "last-name")
    postal_code_input = (By.ID, "postal-code")
    continue_button = (By.ID, "continue")

    finish_button = (By.ID, "finish")
    success_message = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver
        self.common = CommonMethods(driver)

    def enter_checkout_details(self, first_name, last_name, postal_code):
        self.common.send_text(self.first_name_input, first_name)
        self.common.send_text(self.last_name_input, last_name)
        self.common.send_text(self.postal_code_input, postal_code)
        self.common.click(self.continue_button)

    def finish_checkout(self):
        self.common.click(self.finish_button)

    def get_success_message(self):
        return self.common.get_text(self.success_message)
