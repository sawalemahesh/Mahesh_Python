from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pytest
import time
import allure


def test_Xpath():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(chrome_options)
    driver.get("https://practicetestautomation.com/practice-test-login/")

    login = driver.find_element(By.XPATH, "//input[@name='username']")
    login.send_keys("admin@gmail.com")

    password = driver.find_element(By.XPATH, "//input[@name='password']")
    password.send_keys("Wronf@123")

    submit = driver.find_element(By.XPATH, "//button[@id='submit']")
    submit.click()
    time.sleep(3)

    assert "Your username is invalid!" in driver.find_element(By.XPATH, "//div[@id='error']").text
    time.sleep(3)


