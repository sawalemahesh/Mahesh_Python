from POM.pages.login_page import LoginPage
from POM.pages.products_page import ProductsPage
from POM.pages.cart_page import CartPage
from POM.testdata.test_data import TestData
from POM.pages.checkout_page import CheckoutPage



def test_complete_checkout_flow(setup):
    driver = setup

    login_page = LoginPage(driver)
    products_page = ProductsPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    # Login
    login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
    assert products_page.is_products_page_displayed()

    # Add product & go to cart
    products_page.add_product_to_cart()
    products_page.open_cart()
    assert cart_page.is_item_present_in_cart()

    # Checkout
    cart_page.click_checkout()
    checkout_page.enter_checkout_details(
        TestData.FIRST_NAME,
        TestData.LAST_NAME,
        TestData.POSTAL_CODE
    )

    checkout_page.finish_checkout()

    success_message = checkout_page.get_success_message()
    assert TestData.ORDER_SUCCESS_MESSAGE in success_message
