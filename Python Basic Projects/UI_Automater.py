import asyncio
import threading
import time
from pathlib import Path
from flask import Flask, render_template_string, request, redirect
from playwright.async_api import async_playwright

app = Flask(__name__)

URL_FILE = Path("urls.txt")
SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

running = False

# number of tabs per browser
TAB_COUNT = 4

# refresh interval for live preview
REFRESH_SECONDS = 5

# -------------------------
# HTML DASHBOARD
# -------------------------

HTML = """
<!doctype html>
<title>Live Browser Dashboard</title>

<meta http-equiv="refresh" content="{{refresh}}">

<h2>🌐 Live Browser Dashboard</h2>

<form method="post" action="/add">
    <input name="url" placeholder="Enter website URL" size="50">
    <button>Add</button>
</form>

<form method="post" action="/start">
    <button>▶ Start</button>
</form>

<form method="post" action="/stop">
    <button>⏹ Stop</button>
</form>

<h3>Saved Links</h3>
<ul>
{% for url in urls %}
<li>{{url}}</li>
{% endfor %}
</ul>

<h3>Live Tabs Preview</h3>
{% for img in images %}
<div style="margin-bottom:20px">
    <img src="/shots/{{img}}?t={{timestamp}}" width="450"><br>
    <small>{{img}}</small>
</div>
{% endfor %}
"""

# -------------------------
# UTILITIES
# -------------------------

def load_urls():
    if URL_FILE.exists():
        return URL_FILE.read_text().splitlines()
    return []

def save_url(url):
    with open(URL_FILE, "a") as f:
        f.write(url + "\n")

# -------------------------
# PLAYWRIGHT MULTI-TAB ENGINE
# -------------------------

async def run_browser():
    global running

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        while running:
            urls = load_urls()
            if not urls:
                await asyncio.sleep(2)
                continue

            context = await browser.new_context()

            pages = []
            for i in range(TAB_COUNT):
                page = await context.new_page()
                pages.append(page)

            # open URLs in tabs
            for i, page in enumerate(pages):
                url = urls[i % len(urls)]
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                except:
                    pass

            # live preview loop
            preview_cycles = 0
            while running and preview_cycles < 3:
                for i, page in enumerate(pages):
                    try:
                        await page.screenshot(
                            path=SCREENSHOT_DIR / f"tab_{i}.png"
                        )
                    except:
                        pass

                preview_cycles += 1
                await asyncio.sleep(REFRESH_SECONDS)

            await context.close()

        await browser.close()

def start_engine():
    asyncio.run(run_browser())

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    urls = load_urls()
    images = sorted(p.name for p in SCREENSHOT_DIR.glob("*.png"))
    return render_template_string(
        HTML,
        urls=urls,
        images=images,
        refresh=REFRESH_SECONDS,
        timestamp=int(time.time())
    )

@app.route("/add", methods=["POST"])
def add():
    url = request.form.get("url")
    if url:
        save_url(url)
    return redirect("/")

@app.route("/start", methods=["POST"])
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=start_engine, daemon=True).start()
    return redirect("/")

@app.route("/stop", methods=["POST"])
def stop():
    global running
    running = False
    return redirect("/")

@app.route("/shots/<path:filename>")
def shots(filename):
    return app.send_static_file(f"screenshots/{filename}")

# -------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
