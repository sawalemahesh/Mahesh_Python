import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from Selenium import *
import time


def test_automation():
    Options = webdriver.ChromeOptions()
    Options.add_argument('--incognito')
    Options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=Options)
    driver.get("https://automationexercise.com/")


    signup = driver.find_element(By.XPATH, "//a[@href='/login']").click()

    assert driver.current_url == "https://automationexercise.com/login"

def test_SignUp():
    Options = webdriver.ChromeOptions()
    Options.add_argument('--incognito')
    Options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=Options)
    driver.get("https://automationexercise.com/login")

    name = driver.find_element(By.NAME,'name').send_keys("Mahi")
    email = driver.find_element(By.XPATH, "//input[@data-qa='signup-email']").send_keys("xy@gmppil.com")
    click = driver.find_element(By.XPATH, "//button[@data-qa='signup-button']").click()

    assert driver.current_url == "https://automationexercise.com/signup"


# def test_SignUP_Page():
#     Options = webdriver.ChromeOptions()
#     Options.add_argument('--incognito')
#     Options.add_argument('--start-maximized')
#     driver = webdriver.Chrome(options=Options)
#     driver.get("https://automationexercise.com/signup")
#     os.getenv('Password')
#     os.getenv('Firt_Name')
#     os.getenv('Last_Name')
#     os.getenv('address')
#     os.getenv('mobile_number')
#     os.getenv('zipcode')
#     os.getenv('city')
#
#
#    password = driver.find_element(By.XPATH, "//input[@class = 'form-control']").send_keys()

def test_blog():
    Options = webdriver.ChromeOptions()
    Options.add_argument('--incognito')
    Options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=Options)
    driver.get("https://maheshsawale.blogspot.com/")

    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(100)
    driver.quit()



