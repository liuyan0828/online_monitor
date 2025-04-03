"""
-*- coding: utf-8 -*-
@Time : 3/25/25 
@Author : liuyan
@function : 
"""

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from pages.home_page import HomePage

@pytest.mark.asyncio
async def test_sports_page(page):
    _,page = page
    sports_page = HomePage(page)

    await sports_page.goto()
    await sports_page.cards.first.wait_for()

    # 验证卡片滑动
    x_before = await sports_page.get_card_position()
    await sports_page.swipe_card()
    x_after = await sports_page.get_card_position()
    assert x_after < x_before, f"❌ Card did not move left. x_before={x_before}, x_after={x_after}"

    # 验证页面元素
    await sports_page.verify_elements()

    await page.close()
