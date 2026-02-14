from POM.pages.login_page import LoginPage
from POM.pages.products_page import ProductsPage
from POM.pages.cart_page import CartPage
from POM.testdata.test_data import TestData


def test_product_present_in_cart(setup):
    driver = setup

    login_page = LoginPage(driver)
    products_page = ProductsPage(driver)
    cart_page = CartPage(driver)

    login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
    products_page.add_product_to_cart()
    products_page.open_cart()

    assert cart_page.is_item_present_in_cart(), "Product not found in cart"
