from utils.language_detector import LanguageDetector, Localization


class SyncPage:
    locale = Localization()

    def __init__(self, page):
        self.page = page
        self.lang_detector = LanguageDetector()

    def verify_language(self):
        content = self.page.inner_text('body')
        lang = self.lang_detector.get_lang(content)
        self.locale.set_lang(lang)

    def navigate(self, url):
        self.page.goto(url)

    def type_text(self, selector, text):
        self.page.fill(selector, text)

    def click_element(self, selector):
        self.page.click(selector)

    def get_url(self):
        return self.page.url()

    def wait_for_url(self, url):
        self.page.wait_for_url(f"**{url}")

    def click_and_wait_download(self, selector, timeout=30000):
        with self.page.expect_download(timeout=timeout) as download_info:
            self.page.click(selector)
        download = download_info.value
        return download.path()

    def wait_for_element_visible(self, loc):
        self.page.wait_for_selector(loc, state='visible')

    def get_element_text(self, loc):
        return self.page.query_selector(loc).inner_text()

    def click_element_with_text(self, loc, text):
        self.page.locator(loc).filter(has_text=text).click()
