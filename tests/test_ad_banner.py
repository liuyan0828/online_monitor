"""
-*- coding: utf-8 -*-
@Time : 4/1/25 
@Author : liuyan
@function : 
"""
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_ad_banner():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://sports.sohu.com")

        # 1. 获取所有广告容器
        ad_containers = page.locator("div.pc-ad-common")
        count = await ad_containers.count()
        assert count > 0, "❌ 未检测到广告容器"
        print(f"🎯 共检测到 {count} 个广告容器")

        for i in range(count):
            ad = ad_containers.nth(i)
            await expect(ad).to_be_visible()
            print(f"✅ 第 {i + 1} 个广告容器可见")

            # 2. 校验广告图片是否存在
            ad_images = ad.locator("img")
            img_count = await ad_images.count()
            assert img_count > 0, f"❌ 第 {i + 1} 个广告容器无图片"

            for j in range(img_count):
                ad_img = ad_images.nth(j)
                await expect(ad_img).to_be_visible()
                src = await ad_img.get_attribute("src")
                print(f"📌 第 {i + 1} 个广告，第 {j + 1} 张图片地址: {src}")

            # 3. 校验跳转链接是否正常
            ad_link = ad.locator("a")
            if await ad_link.count() > 0:
                href = await ad_link.get_attribute("href")
                print(f"🔗 广告跳转链接: {href}")

                # 点击并确认跳转页面
                try:
                    async with context.expect_page() as new_page_info:
                        await ad_link.first.click()
                    new_page = await new_page_info.value
                    await new_page.wait_for_load_state("domcontentloaded")
                    assert new_page.url.startswith("http")
                    print(f"🚀 广告点击跳转成功: {new_page.url}")
                    await new_page.close()
                except Exception as e:
                    print(f"⚠️ 广告点击跳转失败: {e}")
            else:
                print(f"ℹ️ 第 {i + 1} 个广告容器无跳转链接")

        await browser.close()
