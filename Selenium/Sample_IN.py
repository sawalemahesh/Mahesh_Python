from selenium import webdriver
import pytest
import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def test_IN():
    driver = webdriver.Chrome()
    chrome_options = Options()
    chrome_options.add_argument('--start-minimized')
    chrome_options.add_argument('--no-sandbox')
    driver.get("https://demoqa.com/")
    assert driver.title == "demosite"

    driver.quit()

def test_IN2():
    assert test_IN.title == "demosite"


