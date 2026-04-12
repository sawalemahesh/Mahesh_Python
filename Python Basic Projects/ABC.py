import asyncio
import random
import logging
import os
from pathlib import Path
from playwright.async_api import async_playwright

# ==============================
# AUTO-DETECT CI (JENKINS)
# ==============================

RUNNING_IN_JENKINS = os.getenv("JENKINS_HOME") is not None
HEADLESS = True if RUNNING_IN_JENKINS else False

# ==============================
# TARGET DOMAIN
# ==============================

TARGET_DOMAIN = "maheshsawale.blogspot.com"

# Search queries users might type
SEARCH_QUERIES = [
    "how to trade in stock market India",
    "AI in stock market prediction",
    "what is machine learning simple explanation",
    "how to start blogging for beginners",
    "ways to reduce electricity bill India",
    "web hosting meaning in Marathi",
    "SEO basics for beginners",
    "investment guide for beginners India",
]

# ==============================
# REALISTIC USER ENVIRONMENT
# ==============================

USER_AGENTS = [
    # Desktop Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0 Safari/537.36",
    # Android
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 Chrome/120.0 Mobile Safari/537.36",
    # iPhone
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile Safari/604.1",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

VIEWPORTS = [
    {"width": 1920, "height": 1080},
    {"width": 1366, "height": 768},
    {"width": 390, "height": 844},
    {"width": 414, "height": 896},
]

# ==============================
# SETTINGS
# ==============================

CONCURRENT_BROWSERS = 2
VISIT_DELAY = (8, 18)
PAGE_TIMEOUT = 45000

SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ==============================
# HUMAN BEHAVIOR FUNCTIONS
# ==============================

async def human_mouse_movements(page):
    size = page.viewport_size
    for _ in range(random.randint(3, 7)):
        await page.mouse.move(
            random.randint(0, size["width"]),
            random.randint(0, size["height"]),
            steps=random.randint(10, 25)
        )
        await asyncio.sleep(random.uniform(0.3, 1.1))

async def natural_scroll(page):
    height = await page.evaluate("document.body.scrollHeight")
    pos = 0

    while pos < height:
        step = random.randint(200, 600)
        pos += step
        await page.mouse.wheel(0, step)
        await asyncio.sleep(random.uniform(0.4, 1.2))

        if random.random() < 0.35:
            await asyncio.sleep(random.uniform(2, 5))

async def click_internal_link(page):
    links = await page.locator("a").all()
    internal = []

    for link in links:
        try:
            href = await link.get_attribute("href")
            if href and TARGET_DOMAIN in href:
                internal.append(link)
        except:
            pass

    if internal and random.random() < 0.6:
        try:
            await random.choice(internal).click()
            await asyncio.sleep(random.uniform(10, 35))
        except:
            pass

# ==============================
# GOOGLE SEARCH FLOW
# ==============================

async def google_search_and_open(page):
    keyword = random.choice(SEARCH_QUERIES)

    logging.info(f"Searching: {keyword}")

    await page.goto("https://www.google.com", wait_until="domcontentloaded")

    # Accept consent popup (if shown)
    try:
        await page.locator("button:has-text('Accept all')").click(timeout=3000)
    except:
        pass

    # Type query like a human
    await page.fill("input[name=q]", "")
    for char in keyword:
        await page.type("input[name=q]", char, delay=random.randint(70, 150))

    await page.keyboard.press("Enter")
    await page.wait_for_timeout(random.randint(2000, 4000))

    # Scroll results
    for _ in range(random.randint(1, 3)):
        await page.mouse.wheel(0, random.randint(300, 900))
        await asyncio.sleep(random.uniform(0.7, 1.8))

    results = await page.locator("a").all()

    for link in results:
        try:
            href = await link.get_attribute("href")
            if href and TARGET_DOMAIN in href:
                await link.click()
                logging.info("Clicked search result")
                return True
        except:
            pass

    logging.info("Result not found on first page")
    return False

# ==============================
# VISIT SESSION
# ==============================

async def visit_session(page, sid):
    found = await google_search_and_open(page)

    if not found:
        return

    await human_mouse_movements(page)
    await natural_scroll(page)
    await click_internal_link(page)

    # realistic dwell time
    await asyncio.sleep(random.uniform(30, 90))

    await page.screenshot(path=SCREENSHOT_DIR / f"{sid}.png")

# ==============================
# WORKER
# ==============================

async def worker(worker_id):
    while True:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=HEADLESS,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                    ],
                )

                context = await browser.new_context(
                    user_agent=random.choice(USER_AGENTS),
                    viewport=random.choice(VIEWPORTS),
                    locale="en-IN",
                    timezone_id="Asia/Kolkata",
                )

                page = await context.new_page()

                session_visits = random.randint(2, 5)
                logging.info(f"Worker {worker_id} session started")

                for i in range(session_visits):
                    sid = f"W{worker_id}-{i}"
                    await visit_session(page, sid)
                    await asyncio.sleep(random.uniform(*VISIT_DELAY))

                await browser.close()

                # pause between sessions
                await asyncio.sleep(random.uniform(30, 120))

        except Exception as e:
            logging.error(f"Worker {worker_id} crashed: {e}")
            await asyncio.sleep(5)

# ==============================
# MAIN
# ==============================

async def main():
    workers = [worker(i) for i in range(CONCURRENT_BROWSERS)]
    await asyncio.gather(*workers)

if __name__ == "__main__":
    asyncio.run(main())