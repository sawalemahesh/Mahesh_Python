from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pytest
import time


def test_Xpath():
    # chrome_options = Options()
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome()
    driver.get("https://maheshsawale.blogspot.com/")

    time.sleep(5)


