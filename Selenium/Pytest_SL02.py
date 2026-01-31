from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pytest
import time
import allure


@allure.title("To verify login")
@allure.description("To verify login ID and Password")
def test_login():
    chrome_options =Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(chrome_options)
    driver.get("https://practicetestautomation.com/practice-test-login/")
    time.sleep(3)


    usernmae = driver.find_element(By.ID, "username")
    usernmae.send_keys("student")

    passw = driver.find_element(By.ID, "password")
    passw.send_keys("Password123")

    submit = driver.find_element(By.ID, "submit")
    submit.click()

    time.sleep(2)

    verify = driver.page_source
    c = driver.current_url
    assert "Congratulations student. You successfully logged in!" in verify
    assert "https://practicetestautomation.com/logged-in-successfully/" in c

@allure.title("To verify login Incorrect user ID and Password")
@allure.description("To verify login using Incorrect User ID and Password")
def test_login_negative01():
    chrome_options =Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(chrome_options)
    driver.get("https://practicetestautomation.com/practice-test-login/")
    time.sleep(3)


    usernmae = driver.find_element(By.ID, "username")
    usernmae.send_keys("mahesh")

    passw = driver.find_element(By.ID, "password")
    passw.send_keys("Password123")

    submit = driver.find_element(By.ID, "submit")
    submit.click()

    time.sleep(2)

    login = driver.find_element(By.ID, "error")
    b = login.text
    assert "Your username is invalid!" in b


@allure.title("To verify login using Incorrect Password")
@allure.description("To verify login using Incorrect Password")
def test_login_negative02():
    chrome_options =Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(chrome_options)
    driver.get("https://practicetestautomation.com/practice-test-login/")
    time.sleep(3)


    usernmae = driver.find_element(By.ID, "username")
    usernmae.send_keys("student")

    passw = driver.find_element(By.ID, "password")
    passw.send_keys("Password12344")

    submit = driver.find_element(By.ID, "submit")
    submit.click()

    time.sleep(2)

    login = driver.find_element(By.ID, "error")
    b = login.text
    assert "Your password is invalid!" in b

