from selenium import webdriver
import pytest
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By




def test_login_module():
    chrome_options = Options()
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options)
    driver.get("https://katalon-demo-cura.herokuapp.com/")

    make_appoinment = driver.find_element(By.ID, "btn-make-appointment")
    make_appoinment.click()

    time.sleep(2)

    usename = driver.find_element(By.ID, "txt-username")
    usename.send_keys("John Doe")

    PASS = driver.find_element(By.NAME, "password")
    PASS.send_keys("ThisIsNotAPassword")

    LOGIN = driver.find_element(By.ID, "btn-login")
    LOGIN.click()

    time.sleep(2)

    assert driver.current_url == "https://katalon-demo-cura.herokuapp.com/#appointment"



def test_login_negitive_module():
    chrome_options = Options()
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options)
    driver.get("https://katalon-demo-cura.herokuapp.com/")

    make_appoinment = driver.find_element(By.ID, "btn-make-appointment")
    make_appoinment.click()

    time.sleep(2)

    usename = driver.find_element(By.ID, "txt-username")
    usename.send_keys("Mahesh")

    PASS = driver.find_element(By.NAME, "password")
    PASS.send_keys("Wrong@123")

    LOGIN = driver.find_element(By.ID, "btn-login")
    LOGIN.click()

    failed = driver.find_element(By.CLASS_NAME, "text-danger")
    c = failed.text()

    assert "Login failed! Please ensure the username and password are valid." ==  c
