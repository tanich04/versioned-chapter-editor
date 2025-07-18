# scraping/scrape_chapter.py

from playwright.sync_api import sync_playwright
import os

def fetch_chapter(url: str, screenshot_dir: str = "screenshots") -> str:
    os.makedirs(screenshot_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # Full page screenshot
        chapter_id = url.strip("/").split("/")[-1]
        screenshot_path = os.path.join(screenshot_dir, f"{chapter_id}.png")
        page.screenshot(path=screenshot_path, full_page=True)

        # Extract main content
        content = page.inner_text("body")

        browser.close()

        return content