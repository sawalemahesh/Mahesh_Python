from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pytest

# @pytest.mark.sanity
@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()



def test_cart(setup):
    driver = setup
    driver.find_element(By.ID, "user-name").send_keys("problem_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    assert "inventory" in driver.current_url
    #
    # your cart test
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(),'Test.allTheThings() T-Shirt (Red)')]")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.find_element(By.XPATH, "//div[contains(text(),'Test.allTheThings() T-Shirt (Red)')]").click()

    assert driver.current_url == 'https://www.saucedemo.com/inventory-item.html?id=4'



