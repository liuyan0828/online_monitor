"""
-*- coding: utf-8 -*-
@Time : 3/31/25 
@Author : liuyan
@function : 
"""
import pytest
from playwright.async_api import async_playwright
from PIL import Image, ImageChops

from pages.home_page import HomePage
from utils.image_compare import compare_images


@pytest.mark.asyncio
async def test_tab_visual_compare(page):
    _, page = page
    sports_page = HomePage(page)

    await sports_page.goto()
    screenshot_paths = await sports_page.switch_tabs_and_screenshot()

    is_different = compare_images(screenshot_paths[0], screenshot_paths[1])
    assert is_different, "两个 Tab 内容相同，切换无效"

