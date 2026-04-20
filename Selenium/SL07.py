from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_google_search():
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")

    # Wait for search box
    wait = WebDriverWait(driver, 10)
    search_box = wait.until(EC.visibility_of_element_located((By.NAME, "q")))

    search_box.send_keys("Playwright")
    search_box.send_keys(Keys.RETURN)

    # Wait for title
    wait.until(EC.title_contains("Playwright"))

    assert "Playwright" in driver.title

    driver.quit()


from playwright.sync_api import sync_playwright

def test_google_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com")

        page.fill("input[name='q']", "Playwright")
        page.press("input[name='q']", "Enter")

        # Auto-wait handles everything
        assert "Playwright" in page.title()

        browser.close()