"""
-*- coding: utf-8 -*-
@Time : 3/31/25 
@Author : liuyan
@function : 
"""
import pytest
from playwright.async_api import async_playwright, expect

@pytest.mark.asyncio
async def test_scroll_to_bottom():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://sports.sohu.com")

        # ===== 滚动到底部 =====
        scroll_height = await page.evaluate("document.body.scrollHeight")
        current_position = 0
        step = 500

        while current_position < scroll_height:
            current_position += step
            await page.evaluate(f"window.scrollTo(0, {current_position})")
            await page.wait_for_timeout(500)
            scroll_height = await page.evaluate("document.body.scrollHeight")

        # 最后确保到达最底部
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1000)

        # ===== 验证底部内容 =====
        footer = page.locator("div.PCBottomCopyright")
        await expect(footer).to_be_visible()
        print("✅ 成功滑动到页面底部，版权信息正常展示")

        await browser.close()
