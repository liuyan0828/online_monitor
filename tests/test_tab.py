"""
-*- coding: utf-8 -*-
@Time : 3/31/25 
@Author : liuyan
@function : 
"""
import pytest
from playwright.async_api import async_playwright
from PIL import Image, ImageChops


def compare_images(img1_path, img2_path):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    diff = ImageChops.difference(img1, img2)
    return diff.getbbox() is not None  # True 表示不同


@pytest.mark.asyncio
async def test_tab_visual_compare():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://sports.sohu.com")

        screenshot_paths = []
        nba_tab_container = page.locator("div.tpl-score-rank").filter(has_text="NBA球队排名")
        tabs = nba_tab_container.locator("div.tpl-filter-tab > div")
        count = await tabs.count()
        assert count >= 2, "没有找到两个 Tab"

        # texts = await tabs.all_text_contents()
        # print(texts)

        for i in range(count):
            tab_text = await tabs.nth(i).inner_text()
            print(f'Tab {i}: {tab_text.strip()}')

            await tabs.nth(i).click()
            await tabs.nth(i).wait_for(state="attached")
            # 等待 loading 消失
            await page.locator("text=内容加载中").wait_for(state="detached", timeout=10000)
            screenshot_path = f"tab_{i}.png"
            await nba_tab_container.screenshot(path=screenshot_path)

            screenshot_paths.append(screenshot_path)
            # print(screenshot_paths)

        # 比对截图
        is_different = compare_images(screenshot_paths[0], screenshot_paths[1])
        assert is_different, "两个 Tab 内容相同，切换无效"

        await browser.close()

