from utils.language_detector import LanguageDetector, Localization


class AsyncPage:
    locale = Localization()

    def __init__(self, page):
        self.page = page
        self.lang_detector = LanguageDetector()

    async def verify_language(self):
        content = await self.page.inner_text('body')
        lang = self.lang_detector.get_lang(content)
        self.locale.set_lang(lang)

    async def navigate(self, url):
        await self.page.goto(url)

    async def type_text(self, selector, text):
        await self.page.fill(selector, text)

    async def click_element(self, selector):
        await self.page.click(selector)

    async def get_url(self):
        return self.page.url

    async def wait_for_url(self, url):
        await self.page.wait_for_url(f"**{url}")

    async def click_and_wait_download(self, selector, timeout=30000):
        async with self.page.expect_download(timeout=timeout) as download_info:
            await self.page.click(selector)
        download = await download_info.value
        file_path = await download.path()
        return file_path

    async def wait_for_element_visible(self, selector):
        await self.page.wait_for_selector(selector, state='visible')

    async def get_element_text(self, selector):
        element_handle = await self.page.query_selector(selector)
        return await element_handle.inner_text()

    async def click_element_with_text(self, loc, text):
        await self.page.locator(loc).filter(has_text=text).click()
