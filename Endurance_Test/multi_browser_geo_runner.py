import asyncio
import random
import time
import logging
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from contextlib import asynccontextmanager

# =====================================================
# LOGGING SETUP
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =====================================================
# CONFIGURATION
# =====================================================

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
SESSION_DURATION = 300
REFRESH_INTERVAL = 60
MAX_RETRIES = 3
HEADLESS = False

# AD CLICK CONFIGURATION
AD_CLICK_PROBABILITY = 0.3  # 30% chance to click ads
MIN_ADS_TO_CLICK = 1
MAX_ADS_TO_CLICK = 3
AD_CLICK_DELAY = 2  # Seconds to wait after ad click

# Common ad selectors for Blogspot/AdSense
AD_SELECTORS = [
    "iframe[src*='googleads']",
    "iframe[src*='adservice']",
    "div[data-ad-slot]",
    "ins.adsbygoogle",
    ".adsbygoogle",
    "iframe.google_ads_iframe",
    "a[href*='google']",
    "div.ads",
    "div.advertisement",
    "[role='region'][aria-label*='ad']",
]


# =====================================================
# HUMAN-LIKE SMOOTH SCROLL
# =====================================================

async def structured_scroll(page):
    """Scroll down and up smoothly with error handling"""
    try:
        # Scroll down
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

        # Scroll back up
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
        logger.warning(f"Scroll error: {e}")


# =====================================================
# RANDOM ADS CLICK FUNCTION
# =====================================================

async def find_all_ads(page):
    """Find all clickable ad elements on the page"""
    ads = []

    try:
        # Try each selector and collect all matching elements
        for selector in AD_SELECTORS:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    logger.info(f"Found {len(elements)} ads with selector: {selector}")
                    ads.extend(elements)
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")

        # Also try to find links with ad-like attributes
        try:
            ad_links = await page.query_selector_all('a[href*="doubleclick"], a[href*="googlesyndication"]')
            if ad_links:
                logger.info(f"Found {len(ad_links)} ad links")
                ads.extend(ad_links)
        except:
            pass

        return ads

    except Exception as e:
        logger.error(f"Error finding ads: {e}")
        return []


async def click_random_ads(page):
    """Click random ads on the page"""
    try:
        # Decide if we should click ads based on probability
        if random.random() > AD_CLICK_PROBABILITY:
            logger.info("Skipping ad clicks this round")
            return 0

        # Find all ads
        ads = await find_all_ads(page)

        if not ads:
            logger.info("No ads found on this page")
            return 0

        # Determine how many ads to click
        num_ads_to_click = random.randint(MIN_ADS_TO_CLICK, min(MAX_ADS_TO_CLICK, len(ads)))
        logger.info(f"Attempting to click {num_ads_to_click} out of {len(ads)} available ads")

        # Randomly select ads to click
        selected_ads = random.sample(ads, num_ads_to_click)
        clicked_count = 0

        for ad in selected_ads:
            try:
                # Scroll element into view
                await ad.scroll_into_view_if_needed()
                await asyncio.sleep(random.uniform(0.5, 1.5))

                # Check if element is visible and enabled
                is_visible = await ad.is_visible()
                is_enabled = await ad.is_enabled()

                if is_visible and is_enabled:
                    # Move mouse to element before clicking (human-like behavior)
                    await page.mouse.move_to_element(ad)
                    await asyncio.sleep(random.uniform(0.3, 0.8))

                    # Click the ad
                    await ad.click()
                    clicked_count += 1
                    logger.info(f"✓ Clicked ad #{clicked_count}")

                    # Wait before clicking next ad
                    await asyncio.sleep(AD_CLICK_DELAY)
                else:
                    logger.debug(f"Ad not visible/enabled (visible: {is_visible}, enabled: {is_enabled})")

            except Exception as e:
                logger.warning(f"Failed to click ad: {e}")
                continue

        logger.info(f"Successfully clicked {clicked_count} ads")
        return clicked_count

    except Exception as e:
        logger.error(f"Error in click_random_ads: {e}")
        return 0


async def wait_for_ad_page(page, timeout=10):
    """Wait for the ad landing page to load"""
    try:
        await page.wait_for_load_state("load", timeout=timeout * 1000)
        logger.info("Ad page loaded")

        # Simulate reading the ad page
        read_time = random.uniform(3, 8)
        logger.info(f"Spending {read_time:.1f}s on ad page")
        await asyncio.sleep(read_time)

        # Go back to original page
        try:
            await page.go_back(wait_until="load", timeout=30000)
            logger.info("Returned to original page")
            await asyncio.sleep(2)
        except Exception as e:
            logger.warning(f"Could not go back: {e}")

    except Exception as e:
        logger.warning(f"Ad page load timeout or error: {e}")
        try:
            await page.go_back()
        except:
            pass


# =====================================================
# PAGE VISIT WITH RETRY LOGIC
# =====================================================

async def visit_url(page, url, max_retries=MAX_RETRIES):
    """Visit URL with retry mechanism and ad clicking"""
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Visiting {url} (Attempt {attempt}/{max_retries})")
            await page.goto(url, wait_until="load", timeout=60000)

            # Scroll the page
            await structured_scroll(page)

            # Try to click ads
            await asyncio.sleep(random.uniform(1, 3))
            ads_clicked = await click_random_ads(page)

            if ads_clicked > 0:
                # If ads were clicked, wait for page to stabilize
                await asyncio.sleep(2)

            return True

        except Exception as e:
            logger.error(f"Failed to visit {url}: {e}")
            if attempt < max_retries:
                await asyncio.sleep(5 * attempt)
            else:
                return False

    return False


# =====================================================
# BROWSER CONTEXT MANAGER
# =====================================================

@asynccontextmanager
async def create_browser_context(playwright, browser_name, geo_settings):
    """Context manager for proper browser cleanup"""
    browser = None
    context = None
    page = None

    try:
        browser_type = getattr(playwright, browser_name)
        browser = await browser_type.launch(
            headless=HEADLESS,
            args=["--disable-dev-shm-usage"]
        )

        context = await browser.new_context(
            locale=geo_settings["locale"],
            timezone_id=geo_settings["timezone"],
            geolocation={
                "latitude": geo_settings["latitude"],
                "longitude": geo_settings["longitude"],
            },
            permissions=["geolocation"],
            ignore_https_errors=True,
        )

        page = await context.new_page()
        yield page

    except Exception as e:
        logger.error(f"Browser context creation failed: {e}")
        raise
    finally:
        if page:
            await page.close()
        if context:
            await context.close()
        if browser:
            await browser.close()
        logger.info(f"{browser_name} session closed")


# =====================================================
# SINGLE SESSION
# =====================================================

async def run_single_cycle(playwright, browser_name, geo_settings):
    """Run a single browser session"""
    try:
        logger.info(f"Starting {browser_name} session")

        async with create_browser_context(playwright, browser_name, geo_settings) as page:
            session_start = time.time()
            visit_count = 0
            total_ads_clicked = 0

            while time.time() - session_start < SESSION_DURATION:
                url = random.choice(URLS)

                if await visit_url(page, url):
                    visit_count += 1

                # Random delay to appear more human-like
                delay = random.uniform(REFRESH_INTERVAL * 0.8, REFRESH_INTERVAL * 1.2)
                await asyncio.sleep(delay)

            elapsed = time.time() - session_start
            logger.info(
                f"{browser_name} session completed - "
                f"Duration: {elapsed:.1f}s, Visits: {visit_count}, Ads Clicked: {total_ads_clicked}"
            )

    except Exception as e:
        logger.error(f"Session error for {browser_name}: {e}")


# =====================================================
# MAIN CONTROLLER
# =====================================================

async def main():
    """Main orchestration function"""
    geo_settings = GEO_SETTINGS.get(SELECTED_GEO)

    if not geo_settings:
        logger.error(f"Invalid geo setting: {SELECTED_GEO}")
        return

    # Calculate end time
    total_runtime_seconds = TOTAL_RUN_HOURS * 60 * 60
    end_time = datetime.now() + timedelta(seconds=total_runtime_seconds)

    logger.info(f"Starting scraper for {TOTAL_RUN_HOURS} hours")
    logger.info(f"Geo: {SELECTED_GEO}, End time: {end_time}")
    logger.info(f"Ad click probability: {AD_CLICK_PROBABILITY * 100}%")

    cycle_count = 0

    async with async_playwright() as playwright:
        while datetime.now() < end_time:
            cycle_count += 1
            logger.info(f"\n{'=' * 50}")
            logger.info(f"Starting Cycle #{cycle_count}")
            logger.info(f"{'=' * 50}\n")

            try:
                # Run all browsers in parallel
                tasks = [
                    run_single_cycle(playwright, config["name"], geo_settings)
                    for config in BROWSER_CONFIG
                ]

                await asyncio.gather(*tasks, return_exceptions=True)

                # Cool-down between cycles
                logger.info("Cycle finished. Waiting 5 seconds before restart...\n")
                await asyncio.sleep(5)

            except Exception as e:
                logger.error(f"Cycle error: {e}")
                await asyncio.sleep(10)

    logger.info(f"\nScraper completed after {cycle_count} cycles")


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Scraper interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)