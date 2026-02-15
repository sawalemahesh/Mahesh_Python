import asyncio
import random
import logging
from playwright.async_api import async_playwright

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

CONCURRENT_BROWSERS = 2      # increase slowly (2 → 5 → 10)
PAGES_PER_BROWSER = 3        # pages per browser
HEADLESS = False             # TRUE = background mode
PAGE_TIMEOUT = 45000         # 45 sec timeout
DELAY_BETWEEN_VISITS = (5, 15)

# ==============================
# LOGGING
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ==============================
# HUMAN-LIKE SCROLL
# ==============================

async def smooth_scroll(page):
    try:
        await page.evaluate("""
            async () => {
                const distance = document.body.scrollHeight;
                const step = distance / 30;
                for (let i = 0; i < 30; i++) {
                    window.scrollBy(0, step);
                    await new Promise(r => setTimeout(r, 150));
                }
            }
        """)
        await asyncio.sleep(random.uniform(1,2))

        await page.evaluate("window.scrollTo(0, 0)")
    except:
        pass

# ==============================
# PAGE VISIT
# ==============================

async def visit_page(page, url, session_id):
    try:
        logging.info(f"[{session_id}] Visiting: {url}")

        await page.goto(
            url,
            timeout=PAGE_TIMEOUT,
            wait_until="domcontentloaded"   # avoids load timeout
        )

        await smooth_scroll(page)

        await asyncio.sleep(random.uniform(3,6))

    except Exception as e:
        logging.warning(f"[{session_id}] Error: {e}")

# ==============================
# WORKER (ONE BROWSER)
# ==============================

async def browser_worker(worker_id):
    while True:  # run forever
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=HEADLESS,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-gpu",
                        "--no-sandbox"
                    ]
                )

                context = await browser.new_context()
                pages = [await context.new_page() for _ in range(PAGES_PER_BROWSER)]

                logging.info(f"Browser {worker_id} started")

                while True:
                    tasks = []
                    for i, page in enumerate(pages):
                        url = random.choice(URLS)
                        session_id = f"{worker_id}-{i}"
                        tasks.append(visit_page(page, url, session_id))

                    await asyncio.gather(*tasks)

                    await asyncio.sleep(random.uniform(*DELAY_BETWEEN_VISITS))

        except Exception as e:
            logging.error(f"Browser {worker_id} crashed: {e}")
            await asyncio.sleep(5)

# ==============================
# MAIN LOOP
# ==============================

async def main():
    workers = [
        browser_worker(i)
        for i in range(CONCURRENT_BROWSERS)
    ]

    await asyncio.gather(*workers)

if __name__ == "__main__":
    asyncio.run(main())
