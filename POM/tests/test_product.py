from POM.pages.login_page import LoginPage
from POM.pages.products_page import ProductsPage
from POM.testdata.test_data import TestData


def test_add_product_to_cart(setup):
    driver = setup

    login_page = LoginPage(driver)
    products_page = ProductsPage(driver)

    login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)

    assert products_page.is_products_page_displayed()

    products_page.add_product_to_cart()
