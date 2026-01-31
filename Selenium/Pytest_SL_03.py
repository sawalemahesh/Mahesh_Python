import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def test_demo01():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(chrome_options)
    driver.get("https://demoqa.com/webtables")

    add =driver.find_element(By.ID, "addNewRecordButton")
    add.click()

    first_name = driver.find_element(By.ID, "firstName")
    first_name.send_keys("Mahesh")

    last_name = driver.find_element(By.ID, "lastName")
    last_name.send_keys("Shubham")

    email = driver.find_element(By.ID, "userEmail")
    email.send_keys("abc@gmail.com")

    age = driver.find_element(By.ID, "age")
    age.send_keys("40")

    salary = driver.find_element(By.ID, "salary")
    salary.send_keys("50000")

    department = driver.find_element(By.ID, "department")
    department.send_keys("ABC")

    sumbmit =driver.find_element(By.ID, "submit")
    sumbmit.click()

    find_text = driver.page_source

    assert "Mahesh" in find_text