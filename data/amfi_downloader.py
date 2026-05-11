from playwright.sync_api import sync_playwright
import os

DOWNLOAD_DIR = "data/files"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
def download_latest_portfolio():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        page.goto("https://www.amfiindia.com/online-center/portfolio-disclosure")