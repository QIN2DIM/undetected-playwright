# -*- coding: utf-8 -*-
# Time       : 2022/10/24 13:23
# Author     : QIN2DIM
# GitHub     : https://github.com/QIN2DIM
# Description:
import logging
import sys
from datetime import datetime
from enum import Enum

from playwright.sync_api import sync_playwright, Page, Route

from undetected_playwright import Tarnished

logging.basicConfig(
    level=logging.DEBUG, stream=sys.stdout, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ViewMode(str, Enum):
    new = "new"
    headless = "headless"
    headful = "headful"


def _hijacker(route: Route):
    logging.debug(f"{route.request.method} {route.request.url}")
    route.continue_()


def worker(page: Page, view_mode: ViewMode | None = None):
    logging.info(f"Worker started - {view_mode=}")

    page.route("**/*", _hijacker)
    page.goto("https://bot.sannysoft.com/", wait_until="networkidle")

    # Save screenshot
    _now = datetime.now().strftime("%Y-%m-%d")
    if view_mode:
        _suffix = f"-view-{view_mode}"
    else:
        _suffix = f"-view-{datetime.now().strftime('%H%M%S')}"
    page.screenshot(path=f"result/{_now}/sannysoft{_suffix}.png", full_page=True)

    logging.info(f"Worker finished - {view_mode=}")


def bytedance(view_mode: ViewMode):
    with sync_playwright() as p:
        match view_mode:
            case "new":
                args = ["--headless=new", "--dump-dom"]
                browser = p.chromium.launch(args=args)
            case "headless":
                browser = p.chromium.launch(headless=True)
            case _:
                browser = p.chromium.launch(headless=False)

        context = browser.new_context(locale="en-US")
        Tarnished.apply_stealth(context)

        page = context.new_page()
        worker(page, view_mode)

        browser.close()


def main():
    bytedance(ViewMode.new)
    bytedance(ViewMode.headful)
    bytedance(ViewMode.headless)


if __name__ == "__main__":
    main()
