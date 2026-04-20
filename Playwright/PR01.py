from playwright.sync_api import sync_playwright

def test_login():
    browser = sync_playwright().start().chromium.launch(headless = False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://app.vwo.com/#/login')
    page.wait_for_load_state('networkidle')


