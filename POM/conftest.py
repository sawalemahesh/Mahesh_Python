import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/login")
    driver.maximize_window()
    yield driver
    driver.quit()
