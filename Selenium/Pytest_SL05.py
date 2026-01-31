from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time
import allure


def test_OrangeHRM():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(chrome_options)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    WebDriverWait(driver,timeout=5).until(visibility_of_element_located(By.XPATH,"//button[@type='submit']"))

    login = driver.find_element(By.XPATH,"//input[@name='username']")
    login.send_keys("Admin")

    passw= driver.find_element(By.XPATH,"//input[@name='password']")
    passw.send_keys("admin123")

    submit= driver.find_element(By.XPATH,"//button[@type='submit']")
    submit.click()

    assert driver.current_url== "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"

    time.sleep(3)


    time.sleep(3)

