from selenium.webdriver.common.by import By
from POM.utilities import common_methods as CommonMethods


class ProductsPage:

    page_title = (By.CLASS_NAME, "title")
    add_to_cart_button = (By.ID, "add-to-cart-sauce-labs-backpack")
    cart_icon = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver
        self.common = CommonMethods(driver)

    def is_products_page_displayed(self):
        return self.common.is_element_visible(self.page_title)

    def add_product_to_cart(self):
        self.common.click(self.add_to_cart_button)

    def open_cart(self):
        self.common.click(self.cart_icon)
