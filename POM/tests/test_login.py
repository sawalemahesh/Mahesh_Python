from POM.pages.login_page import LoginPage
from POM.pages.products_page import ProductsPage
from POM.testdata.test_data import TestData


def test_valid_login(setup):
    driver = setup
    login_page = LoginPage(driver)
    products_page = ProductsPage(driver)

    login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)

    assert products_page.is_products_page_displayed(), "Login failed: Products page not displayed"


def test_invalid_login(setup):
    driver = setup
    login_page = LoginPage(driver)

    login_page.login(TestData.INVALID_USERNAME, TestData.INVALID_PASSWORD)

    error_msg = login_page.get_error_message()
    assert TestData.LOGIN_ERROR_MESSAGE in error_msg
