"""
-*- coding: utf-8 -*-
@Time : 3/25/25 
@Author : liuyan
@function : 
"""

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright, expect


@pytest_asyncio.fixture(scope="function")
async def browser_context():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    yield context
    await browser.close()
    await playwright.stop()


@pytest.mark.asyncio
async def test_sports_page(browser_context):
    page = await browser_context.new_page()
    await page.goto("https://sports.sohu.com")

    # 等待卡片加载
    cards = page.locator("a.top-match-card-item")
    await cards.first.wait_for()

    # 获取第一张卡片的 x 坐标 (点击前)
    box_before = await cards.nth(0).bounding_box()
    x_before = box_before["x"]
    print(f"Before click: x = {x_before}")

    # 点击 swiper-next 按钮
    next_btn = page.locator("div.swiper-next")
    await next_btn.click()
    await page.wait_for_timeout(800)  # 等待动画完成

    # 获取第一张卡片的 x 坐标 (点击后)
    box_after = await cards.nth(0).bounding_box()
    x_after = box_after["x"]
    print(f"After click: x = {x_after}")

    # ✅ 验证位置是否左移
    assert x_after < x_before, f"❌ Card did not move left. x_before={x_before}, x_after={x_after}"
    print(f"✅ Card moved left from {x_before} → {x_after}")

    await expect(page.locator('.firstChannelText')).to_have_text("体育")
    assert "体育" in await page.locator('.firstChannelText').inner_text(), "标题不包含 '体育'"

    nav_items = page.locator("a.navigation-head-list-a")
    assert await nav_items.count() >= 5

    expected_items = ['新闻', '体育', '汽车', '房产', '旅游', '教育', '时尚', '科技', '财经', '娱乐', '母婴', '更多 icon_Unfold']
    for text in expected_items:
        item = page.locator("a.navigation-head-list-a", has_text=text)
        await expect(item).to_be_visible()
        await expect(item).to_have_text(text)

    button = page.locator('a.wza-btn-new', has_text="无障碍")
    await expect(button).to_be_visible()

    login_btn = page.locator('a[data-role="login-btn"]', has_text="登录")
    await expect(login_btn).to_be_visible()

    search_input = page.locator('input.search-input')
    await expect(search_input).to_be_visible()


    await page.close()
'''
import pytest
from playwright.sync_api import Page, sync_playwright
from playwright.sync_api import expect

@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        browser.close()

def test_sports_page(browser_context):
    page = browser_context.new_page()
    page.goto("https://sports.sohu.com")

    expect(page.locator('.firstChannelText')).to_have_text("体育")
    # print(page.locator('.firstChannelText').inner_text())

    assert "体育" in page.locator('.firstChannelText').inner_text(), "标题不包含 '体育'"

    nav_items = page.locator("a.navigation-head-list-a")
    # print(nav_items.all_inner_texts())
    assert nav_items.count() >= 5  # 举例：确保至少有5个导航项

    expected_items = ['新闻', '体育', '汽车', '房产', '旅游', '教育', '时尚', '科技', '财经', '娱乐', '母婴', '更多 icon_Unfold']

    for text in expected_items:
        item = page.locator("a.navigation-head-list-a", has_text=text)
        expect(item).to_be_visible()
        expect(item).to_have_text(text)
        # print(f"✅ 导航项 '{text}' 正常展示")

    # 精准定位“无障碍”按钮
    button = page.locator('a.wza-btn-new', has_text="无障碍")
    expect(button).to_be_visible()
    # print("✅ '无障碍' 按钮正确展示")

    button = page.locator('a[data-role="login-btn"]', has_text="登录")
    expect(button).to_be_visible()
    # print("✅ '登录' 按钮正确展示")

    search_input = page.locator('input.search-input')
    expect(search_input).to_be_visible()
    # print("✅ 搜索框正常显示")

    page.close()
'''