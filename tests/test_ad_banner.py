"""
-*- coding: utf-8 -*-
@Time : 4/1/25 
@Author : liuyan
@function : 
"""
import pytest
from pages.home_page import HomePage


@pytest.mark.asyncio
async def test_ad_banner(page):
    context, page = page
    sports_page = HomePage(page)

    await sports_page.goto()
    await sports_page.check_ads(context)
