"""
-*- coding: utf-8 -*-
@Time : 3/31/25 
@Author : liuyan
@function : 
"""
import pytest

from pages.home_page import HomePage


@pytest.mark.asyncio
async def test_scroll_to_bottom(page):
    _, page = page
    sports_page = HomePage(page)
    try:
        await sports_page.goto()
        await sports_page.scroll_to_bottom()
        await sports_page.verify_footer_visible()
        print("✅ 成功滑动到底部并验证版权信息")
    finally:
        await page.close()
