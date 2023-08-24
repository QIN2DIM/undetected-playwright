# -*- coding: utf-8 -*-
# Time       : 2022/10/24 13:06
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
from pathlib import Path

from playwright.async_api import BrowserContext as ASyncContext
from playwright.sync_api import BrowserContext as SyncContext

enabled_evasions = [
    "chrome.app",
    "chrome.csi",
    "chrome.loadTimes",
    "chrome.runtime",
    "iframe.contentWindow",
    "media.codecs",
    "navigator.hardwareConcurrency",
    "navigator.languages",
    "navigator.permissions",
    "navigator.plugins",
    "navigator.webdriver",
    "sourceurl",
    "webgl.vendor",
    "window.outerdimensions",
]


def stealth_sync(context: SyncContext, **kwargs) -> SyncContext:
    for e in enabled_evasions:
        evasion_code = (
            Path(__file__)
            .parent.joinpath(f"puppeteer-extra-plugin-stealth/evasions/{e}/index.js")
            .read_text(encoding="utf8")
        )
        context.add_init_script(evasion_code)

    return context


async def stealth_async(context: ASyncContext, **kwargs) -> ASyncContext:
    for e in enabled_evasions:
        evasion_code = (
            Path(__file__)
            .parent.joinpath(f"puppeteer-extra-plugin-stealth/evasions/{e}/index.js")
            .read_text(encoding="utf8")
        )
        await context.add_init_script(evasion_code)
    return context
