class TestData:
    """
    Centralized test data for automation framework
    """

    # ---------------- Login Data ----------------
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"

    INVALID_USERNAME = "locked_out_user"
    INVALID_PASSWORD = "wrong_password"

    LOGIN_ERROR_MESSAGE = "Epic sadface: Sorry, this user has been locked out."

    # ---------------- Product Data ----------------
    PRODUCT_NAME = "Sauce Labs Backpack"

    # ---------------- Checkout Data ----------------
    FIRST_NAME = "Mahesh"
    LAST_NAME = "Patil"
    POSTAL_CODE = "411001"

    ORDER_SUCCESS_MESSAGE = "Thank you for your order!"

    # ---------------- URLs ----------------
    LOGIN_URL = "https://www.saucedemo.com/"
    INVENTORY_URL = "https://www.saucedemo.com/inventory.html"
