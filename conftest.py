"""
-*- coding: utf-8 -*-
@Time : 3/25/25 
@Author : liuyan
@function : 
"""
import pytest_asyncio
from playwright.async_api import async_playwright


@pytest_asyncio.fixture
async def page():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    yield context, page
    await context.close()
    await browser.close()
    await playwright.stop()