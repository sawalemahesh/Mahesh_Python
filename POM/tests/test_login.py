from pages.login_page import LoginPage

def test_valid_login(driver):
    login = LoginPage(driver)
    login.login("tomsmith", "SuperSecretPassword!")
    assert "You logged into a secure area!" in login.get_message()


def test_invalid_login(driver):
    login = LoginPage(driver)
    login.login("wronguser", "wrongpass")
    assert "Your username is invalid!" in login.get_message()
