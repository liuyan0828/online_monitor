import pytest
from playwright.async_api import async_playwright
from datetime import datetime
import os
import asyncio

from pages.home_page import HomePage
from utils.report_helper import create_dirs


@pytest.mark.asyncio
async def test_check_links(page):
    context, page = page
    sports_page = HomePage(page)
    await sports_page.goto()

    paths = create_dirs()
    links = await sports_page.get_all_links()
    await sports_page.take_screenshot(paths["screenshot"])

    errors, valid = [], []

    async def check_url(url, retries=2):
        attempt = 0
        while attempt <= retries:
            try:
                response = await context.request.get(url, timeout=10000)
                if response.status == 200:
                    return "valid", f"{url} → 200"
                else:
                    attempt += 1
                    if attempt > retries:
                        return "error", f"{url} → Status: {response.status}"
            except Exception as e:
                attempt += 1
                if attempt > retries:
                    return "error", f"{url} → Error: {e}"
            await asyncio.sleep(1)

    with open(paths["log"], "w", encoding="utf-8") as log:
        log.write(f"Link Check - {paths['timestamp']}\nTotal: {len(links)}\n")

        for url in links:
            status, message = await check_url(url)
            if status == "valid":
                valid.append(message)
                log.write(f"✅ {message}\n")
            else:
                errors.append(message)
                log.write(f"❗️ {message}\n")

    # 生成报告
    with open(paths["report"], "w", encoding="utf-8") as f:
        f.write(f"<html><body><h1>Link Check - {paths['timestamp']}</h1>")
        f.write(f"<img src='../{paths['screenshot']}' width='80%'><hr>")
        if errors:
            f.write(f"<h2 style='color:red;'>❗️ Broken Links ({len(errors)})</h2><ul>")
            for err in errors:
                f.write(f"<li>{err}</li>")
            f.write("</ul>")
        else:
            f.write("<h2 style='color:green;'>✅ All links valid</h2>")
        f.write("<h3>Valid Links:</h3><ul>")
        for v in valid:
            f.write(f"<li>{v}</li>")
        f.write("</ul></body></html>")

    assert not errors, f"Found invalid links. See log: {paths['log']}"