import pytest
from playwright.async_api import async_playwright
from datetime import datetime
import os
import asyncio


@pytest.mark.asyncio
async def test_check_links_html_with_pytest_report(request):
    report_dir = "reports"
    screenshot_dir = "screenshots"
    log_dir = "logs"
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    custom_report_path = os.path.join(report_dir, f"report_{timestamp}.html")
    screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
    log_path = os.path.join(log_dir, f"log_{timestamp}.txt")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://sports.sohu.com")
        await page.screenshot(path=screenshot_path)

        hrefs = await page.eval_on_selector_all(
            "a",
            "elements => elements.map(el => el.href).filter(href => href.startsWith('http'))"
        )

        errors = []
        valid = []

        async def check_url(url, retries=2):
            attempt = 0
            while attempt <= retries:
                try:
                    response = await context.request.get(url, timeout=10000)
                    if response.status == 200:
                        return "valid", f"{url} → Status: 200"
                    else:
                        attempt += 1
                        if attempt > retries:
                            return "error", f"{url} → Status: {response.status}"
                except Exception as e:
                    attempt += 1
                    if attempt > retries:
                        return "error", f"{url} → Error: {e}"
                await asyncio.sleep(1)

        with open(log_path, "w", encoding="utf-8") as log:
            log.write(f"[{timestamp}] Start checking https://sports.sohu.com links\n")
            log.write(f"[{timestamp}] Found {len(hrefs)} links\n")

            for url in hrefs:
                status, message = await check_url(url)
                if status == "valid":
                    valid.append(message)
                    log.write(f"✅ {message}\n")
                else:
                    errors.append(message)
                    log.write(f"❗️ {message}\n")

            log.write(f"\nCheck complete: {len(hrefs)} links, {len(valid)} success, {len(errors)} failed\n")
            log.write(f"Log file: {log_path}\n")
            log.write(f"Custom HTML report: {custom_report_path}\n")

        # Generate custom HTML report
        with open(custom_report_path, "w", encoding="utf-8") as f:
            f.write(f"<html><head><title>Link Check Report {timestamp}</title></head><body>")
            f.write(f"<h1>Link Check Report - {timestamp}</h1>")
            f.write(f"<h2>Page Screenshot:</h2>")
            f.write(f'<img src="../{screenshot_path}" width="80%">')
            f.write("<h2>Results:</h2>")

            if errors:
                f.write(f"<h3 style='color:red;'>❗️ Broken Links ({len(errors)})</h3><ul>")
                for err in errors:
                    f.write(f"<li>{err}</li>")
                f.write("</ul>")
            else:
                f.write("<h3 style='color:green;'>✅ All links valid</h3>")

            f.write("<h3>Valid Links:</h3><ul>")
            for v in valid:
                f.write(f"<li>{v}</li>")
            f.write("</ul>")
            f.write("</body></html>")

        # Attach screenshot to pytest-html report
        if hasattr(request.config, "_html"):
            extra = getattr(request.node, "extra", [])
            extra.append({"name": "screenshot", "content": screenshot_path, "mime_type": "image/png"})
            request.node.extra = extra

        assert not errors, f"Found invalid links. See log: {log_path}"

        await context.close()
        await browser.close()