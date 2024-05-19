# -*- coding: utf-8 -*-
# Time       : 2023/8/24 20:44
# Author     : QIN2DIM
# GitHub     : https://github.com/QIN2DIM
# Description:
import asyncio
import logging
import sys
from datetime import datetime
from enum import Enum

from playwright.async_api import async_playwright, Page, Route

from undetected_playwright import Malenia

logging.basicConfig(
    level=logging.DEBUG, stream=sys.stdout, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ViewMode(str, Enum):
    new = "new"
    headless = "headless"
    headful = "headful"


async def _hijacker(route: Route):
    logging.debug(f"{route.request.method} {route.request.url}")
    await route.continue_()


async def worker(page: Page, view_mode: ViewMode | None = None):
    logging.info(f"Worker started - {view_mode=}")

    await page.route("**/*", _hijacker)
    await page.goto("https://www.nowsecure.nl", wait_until="networkidle")

    # Just for demo
    await page.wait_for_timeout(8000)

    # Save screenshot
    _now = datetime.now().strftime("%Y-%m-%d")
    if view_mode:
        _suffix = f"-view-{view_mode}"
    else:
        _suffix = f"-view-{datetime.now().strftime('%H%M%S')}"
    await page.screenshot(path=f"result/{_now}/cloudflare{_suffix}.png", full_page=True)

    logging.info(f"Worker finished - {view_mode=}")


async def bytedance(view_mode: ViewMode):
    async with async_playwright() as p:
        match view_mode:
            case "new":
                args = ["--headless=new", "--dump-dom"]
                browser = await p.chromium.launch(args=args)
            case "headless":
                browser = await p.chromium.launch(headless=True)
            case _:
                browser = await p.chromium.launch(headless=False)

        context = await browser.new_context(locale="en-US")
        await Malenia.apply_stealth(context)

        page = await context.new_page()
        await worker(page, view_mode)

        await browser.close()


async def main():
    await bytedance(ViewMode.new)
    await bytedance(ViewMode.headful)
    await bytedance(ViewMode.headless)


if __name__ == "__main__":
    asyncio.run(main())
