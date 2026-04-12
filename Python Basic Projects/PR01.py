import asyncio
import random
import logging
import os
from pathlib import Path
from playwright.async_api import async_playwright

# ==============================
# AUTO-DETECT JENKINS
# ==============================

RUNNING_IN_JENKINS = os.getenv("JENKINS_HOME") is not None

# show browser locally, headless in Jenkins
HEADLESS = True if RUNNING_IN_JENKINS else False

# ==============================
# SETTINGS
# ==============================

URLS = [
    "https://maheshsawale.blogspot.com/",
    "https://maheshsawale.blogspot.com/2025/04/how-ai-and-big-data-are-changing-stock.html",
    "https://maheshsawale.blogspot.com/2022/09/how-to-trade-in-stock-market.html",
    "https://maheshsawale.blogspot.com/2024/04/a-comprehensive-guide-to-invest-in.html",
    "https://maheshsawale.blogspot.com/2022/08/5-ways-to-reduce-your-power-bill-by.html",
    "https://maheshsawale.blogspot.com/2024/04/what-is-machine-learning-and-artificial.html",
    "https://maheshsawale.blogspot.com/2022/08/what-is-web-hosting-in-marathi.html",
    "https://maheshsawale.blogspot.com/2022/08/seo.html",
    "https://maheshsawale.blogspot.com/2022/08/blog-post.html",
    "https://maheshsawale.blogspot.com/2022/08/how-to-start-blogging.html",
]

CONCURRENT_BROWSERS = 2
PAGES_PER_BROWSER = 2
VISIT_DELAY = (5, 12)
PAGE_TIMEOUT = 30000

SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

# ==============================
# LOGGING
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info(f"Running in Jenkins: {RUNNING_IN_JENKINS}")
logging.info(f"Headless mode: {HEADLESS}")

# ==============================
# BLOCK HEAVY RESOURCES (FASTER)
# ==============================

async def block_resources(route):
    if route.request.resource_type in ["image", "media", "font"]:
        await route.abort()
    else:
        await route.continue_()

# ==============================
# HUMAN-LIKE SCROLL
# ==============================

async def smooth_scroll(page):
    try:
        await page.evaluate("""
            async () => {
                const height = document.body.scrollHeight;
                const step = height / 25;
                for (let i = 0; i < 25; i++) {
                    window.scrollBy(0, step);
                    await new Promise(r => setTimeout(r, 120));
                }
            }
        """)
        await asyncio.sleep(random.uniform(1,2))
        await page.evaluate("window.scrollTo(0,0)")
    except:
        pass

# ==============================
# VISIT PAGE
# ==============================

async def visit(page, url, sid):
    try:
        logging.info(f"[{sid}] Visiting {url}")

        await page.goto(
            url,
            timeout=PAGE_TIMEOUT,
            wait_until="domcontentloaded"
        )

        await smooth_scroll(page)

        # screenshot helps confirm execution in Jenkins
        await page.screenshot(path=SCREENSHOT_DIR / f"{sid}.png")

        await asyncio.sleep(random.uniform(2,5))

    except Exception as e:
        logging.warning(f"[{sid}] Error: {e}")

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
                        "--disable-gpu"
                    ]
                )

                context = await browser.new_context()
                await context.route("**/*", block_resources)

                pages = [await context.new_page() for _ in range(PAGES_PER_BROWSER)]

                logging.info(f"Worker {worker_id} started")

                while True:
                    tasks = []
                    for i, page in enumerate(pages):
                        url = random.choice(URLS)
                        sid = f"W{worker_id}-P{i}"
                        tasks.append(visit(page, url, sid))

                    await asyncio.gather(*tasks)
                    await asyncio.sleep(random.uniform(*VISIT_DELAY))

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
