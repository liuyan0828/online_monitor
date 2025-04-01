"""
-*- coding: utf-8 -*-
@Time : 3/26/25 
@Author : liuyan
@function : 
"""
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_search_functionality():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://sports.sohu.com")

        # 1️⃣ 定位搜索框
        search_input = page.locator('input.search-input')

        # ✅ 1. 确认 placeholder 有文字（动态）
        placeholder = await search_input.get_attribute("placeholder")
        assert placeholder is not None and len(placeholder.strip()) > 0
        print(f"✅ Placeholder text: {placeholder}")

        # 直接点击icon带placeholder搜索词跳转
        async with context.expect_page() as new_page_info:
            await page.locator("div.search-icon.search-btn-wrap").click()

        new_page = await new_page_info.value  # 🎯 新页面对象
        await new_page.wait_for_load_state("domcontentloaded")

        # 获取新页面 URL
        new_url = new_page.url

        # 发起 API 请求校验状态码
        response = await context.request.get(new_url)
        assert response.status == 200
        print(f"✅ New page URL: {new_url} → Status: {response.status}")

        # ✅ 检查新页面标题或URL是否包含搜索词
        assert placeholder in await new_page.title()
        print("✅ 搜索跳转成功，搜索结果页已打开")

        # ✅ 2. 点击激活搜索框
        await search_input.click(force=True)

        # ✅ 3. 清除原内容并输入其他内容
        await search_input.fill("NBA最新战报")
        await search_input.press("Enter")

        # 🧠 等待跳转打开新页面（popup）
        async with context.expect_page() as new_page_info:
            await page.locator("div.search-icon.search-btn-wrap").click()

        new_page = await new_page_info.value  # 🎯 新页面对象
        await new_page.wait_for_load_state("domcontentloaded")

        # ✅ 检查新页面标题或URL是否包含搜索词
        assert "NBA" in await new_page.title() or "nba" in await new_page.url.lower()
        print("✅ 搜索跳转成功，搜索结果页已打开")

        await context.close()
        await browser.close()

