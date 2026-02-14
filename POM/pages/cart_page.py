from selenium.webdriver.common.by import By
from POM.utilities import common_methods as CommonMethods


class CartPage:

    cart_item = (By.CLASS_NAME, "inventory_item_name")
    checkout_button = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.common = CommonMethods(driver)

    def is_item_present_in_cart(self):
        return self.common.is_element_visible(self.cart_item)

    def click_checkout(self):
        self.common.click(self.checkout_button)
