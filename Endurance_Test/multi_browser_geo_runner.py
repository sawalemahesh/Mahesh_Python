import asyncio
import random
import time
from playwright.async_api import async_playwright

# =====================================================
# CONFIGURATION
# =====================================================

URLS = [
    "https://maheshsawale.blogspot.com/",
    "https://maheshsawale.blogspot.com/2025/04/how-ai-and-big-data-are-changing-stock.html",
    "https://maheshsawale.blogspot.com/2022/09/how-to-trade-in-stock-market.html"
]

SELECTED_GEO = "IN"

GEO_SETTINGS = {
    "IN": {
        "locale": "en-IN",
        "timezone": "Asia/Kolkata",
        "latitude": 28.6139,
        "longitude": 77.2090,
    },
    "US": {
        "locale": "en-US",
        "timezone": "America/New_York",
        "latitude": 40.7128,
        "longitude": -74.0060,
    },
    "UK": {
        "locale": "en-GB",
        "timezone": "Europe/London",
        "latitude": 51.5074,
        "longitude": -0.1278,
    }
}

BROWSER_CONFIG = [
    {"name": "chromium"},
    {"name": "firefox"},
    {"name": "webkit"},
]

TOTAL_RUN_HOURS = 6
SESSION_DURATION = 300   # 5 minutes per browser session
REFRESH_INTERVAL = 60

# FORCE HEADLESS MODE
HEADLESS = True

# =====================================================
# HUMAN-LIKE SMOOTH SCROLL
# =====================================================

async def structured_scroll(page):
    try:
        await page.evaluate("""
            async () => {
                const scrollHeight = document.body.scrollHeight - window.innerHeight;
                const duration = 6000;
                const start = performance.now();

                return new Promise(resolve => {
                    function animate(currentTime) {
                        const progress = Math.min((currentTime - start) / duration, 1);
                        window.scrollTo(0, scrollHeight * progress);

                        if (progress < 1) {
                            requestAnimationFrame(animate);
                        } else {
                            resolve();
                        }
                    }
                    requestAnimationFrame(animate);
                });
            }
        """)

        await asyncio.sleep(2)

        await page.evaluate("""
            async () => {
                const scrollHeight = document.body.scrollHeight - window.innerHeight;
                const duration = 6000;
                const start = performance.now();

                return new Promise(resolve => {
                    function animate(currentTime) {
                        const progress = Math.min((currentTime - start) / duration, 1);
                        window.scrollTo(0, scrollHeight * (1 - progress));

                        if (progress < 1) {
                            requestAnimationFrame(animate);
                        } else {
                            resolve();
                        }
                    }
                    requestAnimationFrame(animate);
                });
            }
        """)

    except Exception as e:
        print("Scroll error:", e)

# =====================================================
# SINGLE SESSION
# =====================================================

async def run_single_cycle(playwright, browser_name, geo_settings):
    print(f"Launching {browser_name} in HEADLESS mode")

    browser_type = getattr(playwright, browser_name)
    browser = await browser_type.launch(headless=HEADLESS)

    context = await browser.new_context(
        locale=geo_settings["locale"],
        timezone_id=geo_settings["timezone"],
        geolocation={
            "latitude": geo_settings["latitude"],
            "longitude": geo_settings["longitude"],
        },
        permissions=["geolocation"]
    )

    page = await context.new_page()
    session_start = time.time()

    while time.time() - session_start < SESSION_DURATION:
        url = random.choice(URLS)
        print(f"{browser_name} loading {url}")

        try:
            await page.goto(url, wait_until="load", timeout=60000)
            await structured_scroll(page)
            await asyncio.sleep(REFRESH_INTERVAL)
            await page.reload()
        except Exception as e:
            print(f"{browser_name} error:", e)
            await asyncio.sleep(5)

    await context.close()
    await browser.close()
    print(f"{browser_name} session completed\n")

# =====================================================
# MAIN CONTROLLER
# =====================================================

async def main():
    geo_settings = GEO_SETTINGS.get(SELECTED_GEO)

    total_runtime_seconds = TOTAL_RUN_HOURS * 60 * 60
    global_start = time.time()

    async with async_playwright() as playwright:
        while time.time() - global_start < total_runtime_seconds:
            print("\n===== Starting New Cycle =====\n")

            tasks = [
                run_single_cycle(playwright, config["name"], geo_settings)
                for config in BROWSER_CONFIG
            ]

            await asyncio.gather(*tasks)

            print("\nCycle finished. Restarting browsers...\n")
            await asyncio.sleep(5)

    print("\nTotal endurance duration completed.\n")

if __name__ == "__main__":
    asyncio.run(main())
