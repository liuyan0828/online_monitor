"""
-*- coding: utf-8 -*-
@Time : 4/2/25
@Author : liuyan
@function :
"""
from playwright.async_api import Page, expect

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.cards = page.locator("a.top-match-card-item")
        self.next_btn = page.locator("div.swiper-next")
        self.title = page.locator('.firstChannelText')
        self.nav_items = page.locator("a.navigation-head-list-a")
        self.accessible_btn = page.locator('a.wza-btn-new', has_text="无障碍")
        self.login_btn = page.locator('a[data-role="login-btn"]', has_text="登录")
        self.search_input = page.locator('input.search-input')
        self.search_icon = page.locator('div.search-icon.search-btn-wrap')
        self.footer = page.locator("div.PCBottomCopyright")
        self.nba_tab_container = page.locator("div.tpl-score-rank").filter(has_text="NBA球队排名")
        self.tabs = self.nba_tab_container.locator("div.tpl-filter-tab > div")
        self.loading = page.locator("text=内容加载中")
        self.ad_containers = page.locator("div.pc-ad-common")

    async def goto(self):
        await self.page.goto("https://sports.sohu.com")

    async def get_card_position(self):
        box = await self.cards.nth(0).bounding_box()
        return box["x"]

    async def swipe_card(self):
        await self.next_btn.click()
        await self.page.wait_for_timeout(800)

    async def verify_elements(self):
        await expect(self.title).to_have_text("体育")
        assert "体育" in await self.title.inner_text()
        assert await self.nav_items.count() >= 5

        expected_items = ['新闻', '体育', '汽车', '房产', '旅游', '教育', '时尚', '科技', '财经', '娱乐', '母婴', '更多 icon_Unfold']
        for text in expected_items:
            item = self.page.locator("a.navigation-head-list-a", has_text=text)
            await expect(item).to_be_visible()
            await expect(item).to_have_text(text)

        await expect(self.accessible_btn).to_be_visible()
        await expect(self.login_btn).to_be_visible()
        await expect(self.search_input).to_be_visible()

    async def scroll_to_bottom(self):
        scroll_height = await self.page.evaluate("document.body.scrollHeight")
        step = 500
        for position in range(0, scroll_height, step):
            await self.page.evaluate(f"window.scrollTo(0, {position})")
            await self.page.wait_for_timeout(300)

    async def verify_footer_visible(self):
        await expect(self.footer).to_be_visible()

    async def get_search_placeholder(self):
        return await self.search_input.get_attribute("placeholder")

    async def search_by_placeholder(self, context):
        async with context.expect_page() as new_page_info:
            await self.search_icon.click()
        new_page = await new_page_info.value
        await new_page.wait_for_load_state("domcontentloaded")
        return new_page

    async def search_by_keyword(self, context, keyword):
        await self.search_input.click(force=True)
        await self.search_input.fill(keyword)
        await self.search_input.press("Enter")

        async with context.expect_page() as new_page_info:
            await self.search_icon.click()
        new_page = await new_page_info.value
        await new_page.wait_for_load_state("domcontentloaded")
        return new_page

    async def switch_tabs_and_screenshot(self):
        screenshot_paths = []
        count = await self.tabs.count()
        assert count >= 2, "没有找到两个 Tab"

        for i in range(count):
            await self.tabs.nth(i).click()
            await self.tabs.nth(i).wait_for(state="attached")
            await self.loading.wait_for(state="detached", timeout=10000)
            screenshot_path = f"tab_{i}.png"
            await self.nba_tab_container.screenshot(path=screenshot_path)
            screenshot_paths.append(screenshot_path)

        return screenshot_paths

    async def check_ads(self, context):
        count = await self.ad_containers.count()
        assert count > 0, "❌ 未检测到广告容器"
        print(f"🎯 共检测到 {count} 个广告容器")

        for i in range(count):
            ad = self.ad_containers.nth(i)
            await expect(ad).to_be_visible()
            print(f"✅ 第 {i + 1} 个广告容器可见")

            # 校验图片
            ad_images = ad.locator("img")
            img_count = await ad_images.count()
            assert img_count > 0, f"❌ 第 {i + 1} 个广告容器无图片"

            for j in range(img_count):
                ad_img = ad_images.nth(j)
                await expect(ad_img).to_be_visible()
                src = await ad_img.get_attribute("src")
                print(f"📌 第 {i + 1} 个广告，第 {j + 1} 张图片地址: {src}")

            # 校验跳转
            ad_link = ad.locator("a")
            if await ad_link.count() > 0:
                href = await ad_link.get_attribute("href")
                print(f"🔗 广告跳转链接: {href}")

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

    async def get_all_links(self):
        return await self.page.eval_on_selector_all(
            "a",
            "elements => elements.map(el => el.href).filter(href => href.startsWith('http'))"
        )

    async def take_screenshot(self, path):
        await self.page.screenshot(path=path)