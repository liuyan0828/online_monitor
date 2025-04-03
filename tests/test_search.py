"""
-*- coding: utf-8 -*-
@Time : 3/26/25 
@Author : liuyan
@function : 
"""
import pytest

from pages.home_page import HomePage


@pytest.mark.asyncio
async def test_search_functionality(page):
    context, page = page
    sports_page = HomePage(page)

    try:
        await sports_page.goto()

        # ✅ 检查 placeholder
        placeholder = await sports_page.get_search_placeholder()
        assert placeholder and len(placeholder.strip()) > 0
        print(f"✅ Placeholder text: {placeholder}")

        # ✅ 直接点击 icon 搜索
        new_page = await sports_page.search_by_placeholder(context)
        new_url = new_page.url
        response = await context.request.get(new_url)
        assert response.status == 200
        assert placeholder in await new_page.title()
        print(f"✅ Placeholder search opened → {new_url}")

        # ✅ 输入自定义关键词搜索
        keyword = "NBA最新战报"
        new_page = await sports_page.search_by_keyword(context, keyword)
        assert "nba" in new_page.url.lower() or "NBA" in await new_page.title()
        print("✅ Keyword search page opened successfully")

    finally:
        await page.close()

