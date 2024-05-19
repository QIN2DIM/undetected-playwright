# -*- coding: utf-8 -*-
# Time       : 2024/5/19 9:52
# Author     : QIN2DIM
# GitHub     : https://github.com/QIN2DIM
# Description:
import webbrowser
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright, Page

from undetected_playwright import Tarnished


def cache_screenshot(page: Page):
    _now = datetime.now().strftime("%Y-%m-%d")
    _suffix = f"-view-new-{datetime.now().strftime('%H%M%S')}"
    path = f"result/{_now}/sannysoft{_suffix}.png"
    page.screenshot(path=path, full_page=True)

    webbrowser.open(f"file://{Path(path).resolve()}")


def main():
    # Chrome 112+
    args = ["--headless=new", "--dump-dom"]

    with sync_playwright() as p:
        browser = p.chromium.launch(args=args)
        context = browser.new_context(locale="en-US")

        # Injecting Context
        Tarnished.apply_stealth(context)
        page = context.new_page()

        page.goto("https://bot.sannysoft.com/", wait_until="networkidle")
        cache_screenshot(page)

        browser.close()


if __name__ == "__main__":
    main()
