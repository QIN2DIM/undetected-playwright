# undetected-playwright

## Usage

1. **Download PyPi package**

   ```bash
   pip install -U undetected-playwright
   ```

2. **Donload dependencies**

   ```bash
   playwright install --with-deps
   ```

3. **Quick started**

   ```python
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
   
   ```

## Demo: SyncPlaywright Sannysoft

```python
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

```



## Demo: AsyncPlaywright CloudFlare

```python
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

```





## Reference

- [berstend/puppeteer-extra](https://github.com/berstend/puppeteer-extra)
- [AtuboDad/playwright_stealth: playwright stealth (github.com)](https://github.com/AtuboDad/playwright_stealth)
- [Granitosaurus/playwright-stealth (github.com)](https://github.com/Granitosaurus/playwright-stealth)
- [diprajpatra/selenium-stealth: Trying to make python selenium more stealthy. (github.com)](https://github.com/diprajpatra/selenium-stealth)
