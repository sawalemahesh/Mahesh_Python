from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def test_login():
    chrome_options = Options()
    # chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(3)
    username = driver.find_element(By.NAME, 'username').send_keys('Admin')
    password = driver.find_element(By.NAME, 'password').send_keys('admin123')
    submit= driver.find_element(By.XPATH, "//button[@type ='submit']").click()
    assert driver.current_url == 'https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index'
    time.sleep(2)
    admin = driver.find_element(By.XPATH, "//span[text()='Admin']").click()
    time.sleep(2)
    add= driver.find_element(By.XPATH, "//button[@type='button']").click()
    user_role = driver.find_element(By.XPATH, "//div[@class = 'oxd-select-text-input']").click()
    ESS = driver.find_element(By.XPATH, "//li[text()='ESS']").click()

