# undetected-playwright

## Usage

1. **Download PyPi package**

   ```bash
   pip install -U undetected-playwright
   ```
2. **Donload dependencies**

   ```bash
   playwright install
   playwright install-deps
   ```

2. **Run the demo**

   ```python
   from playwright.sync_api import BrowserContext, sync_playwright
   
   from undetected_playwright import stealth_sync
   
   headless = True
   
   
   def run(context: BrowserContext):
       page = context.new_page()
       page.goto("https://bot.sannysoft.com/")
   
       _suffix = "-headless" if headless else "-headful"
       page.screenshot(path=f"result/sannysoft{_suffix}.png", full_page=True)
   
   
   def bytedance():
       with sync_playwright() as p:
           browser = p.chromium.launch(headless=headless)
           context = browser.new_context()
           stealth_sync(context)
           run(context)
   
   
   if __name__ == "__main__":
       bytedance()
   ```

   

## Reference

- [berstend/puppeteer-extra](https://github.com/berstend/puppeteer-extra)

- [AtuboDad/playwright_stealth: playwright stealth (github.com)](https://github.com/AtuboDad/playwright_stealth)
- [Granitosaurus/playwright-stealth (github.com)](https://github.com/Granitosaurus/playwright-stealth)

- [diprajpatra/selenium-stealth: Trying to make python selenium more stealthy. (github.com)](https://github.com/diprajpatra/selenium-stealth)
