import asyncio
import random
import argparse
import time
from playwright.async_api import async_playwright

# =====================================================
# 🔹 HARDCODED URL LIST
# =====================================================

URL_LIST = [
    "https://maheshsawale.blogspot.com/",
    # "https://maheshsawale.blogspot.com/p/about-me.html",
    # "https://maheshsawale.blogspot.com/search/label/Automation",
]

# =====================================================
# 🔹 GEO LOCATIONS
# =====================================================

GEO_LOCATIONS = {
    "IN": {"latitude": 20.5937, "longitude": 78.9629},
    "US": {"latitude": 37.0902, "longitude": -95.7129},
    "UK": {"latitude": 55.3781, "longitude": -3.4360},
    "DE": {"latitude": 51.1657, "longitude": 10.4515},
    "SG": {"latitude": 1.3521, "longitude": 103.8198},
}

# =====================================================
# 🔹 DEVICE LIST
# =====================================================

MOBILE_DEVICES = [
    "iPhone 14",
    "Pixel 7",
    "iPad Pro 11"
]

DESKTOP_VIEWPORT = {"width": 1280, "height": 800}

# =====================================================
# 🔹 LOAD PROXIES
# =====================================================

def load_proxies(proxy_file):
    try:
        with open(proxy_file, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except:
        return []

# =====================================================
# 🔹 AUTO SCROLL
# =====================================================

async def auto_scroll(page, duration=15):
    end_time = time.time() + duration
    while time.time() < end_time:
        await page.evaluate("window.scrollBy(0, window.innerHeight)")
        await asyncio.sleep(1)

# =====================================================
# 🔹 SESSION FUNCTION
# =====================================================

async def run_session(playwright, config, session_id):

    proxy = random.choice(config["proxies"]) if config["proxies"] else None
    geo = GEO_LOCATIONS.get(config["geo"], GEO_LOCATIONS["US"])

    browser_type = random.choice(
        [playwright.chromium, playwright.firefox, playwright.webkit]
    )

    # Firefox does NOT support mobile emulation
    if browser_type == playwright.firefox:
        device_name = "Desktop"
        use_mobile = False
    else:
        device_name = random.choice(["Desktop"] + MOBILE_DEVICES)
        use_mobile = device_name != "Desktop"

    print(f"🚀 Session {session_id} | Browser: {browser_type.name} | Device: {device_name}")

    browser = await browser_type.launch(headless=config["headless"])

    context_args = {
        "geolocation": geo,
        "permissions": ["geolocation"],
        "locale": "en-US",
    }

    if proxy:
        context_args["proxy"] = {"server": proxy}

    # Apply device safely
    if use_mobile:
        device = playwright.devices.get(device_name)
        context_args.update(device)
    else:
        context_args["viewport"] = DESKTOP_VIEWPORT

    context = await browser.new_context(**context_args)
    page = await context.new_page()

    start_time = time.time()

    try:
        while True:

            # Max runtime stop
            if config["max_runtime"] and (time.time() - start_time) > config["max_runtime"]:
                print(f"⏹ Session {session_id} reached max runtime")
                break

            if config["random_url"]:
                url = random.choice(URL_LIST)
                print(f"🌍 Session {session_id} loading: {url}")

                await page.goto(url, timeout=60000)
                await auto_scroll(page, config["scroll_duration"])
                await asyncio.sleep(config["refresh_interval"])

            else:
                for url in URL_LIST:

                    if config["max_runtime"] and (time.time() - start_time) > config["max_runtime"]:
                        break

                    print(f"🌍 Session {session_id} loading: {url}")
                    await page.goto(url, timeout=60000)
                    await auto_scroll(page, config["scroll_duration"])
                    await asyncio.sleep(config["refresh_interval"])

    except Exception as e:
        print(f"❌ Session {session_id} Error: {e}")

    finally:
        try:
            await context.close()
        except:
            pass

        try:
            await browser.close()
        except:
            pass

        print(f"✅ Session {session_id} Closed")

# =====================================================
# 🔹 MAIN FUNCTION
# =====================================================

async def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--geo", default="US")
    parser.add_argument("--sessions", type=int, default=3)
    parser.add_argument("--refresh_interval", type=int, default=30)
    parser.add_argument("--scroll_duration", type=int, default=15)
    parser.add_argument("--proxy_file", default="proxies.txt")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--random_url", action="store_true")
    parser.add_argument("--max_runtime", type=int, default=0,
                        help="Max runtime per session in seconds (0 = infinite)")

    args = parser.parse_args()

    config = {
        "geo": args.geo,
        "refresh_interval": args.refresh_interval,
        "scroll_duration": args.scroll_duration,
        "proxies": load_proxies(args.proxy_file),
        "headless": args.headless,
        "random_url": args.random_url,
        "max_runtime": args.max_runtime
    }

    async with async_playwright() as playwright:

        tasks = [
            run_session(playwright, config, i + 1)
            for i in range(args.sessions)
        ]

        await asyncio.gather(*tasks, return_exceptions=True)

# =====================================================
# 🔹 RUN
# =====================================================

if __name__ == "__main__":
    asyncio.run(main())
