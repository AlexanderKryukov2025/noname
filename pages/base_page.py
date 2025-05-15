class BasePage:
    def __init__(self, page):
        self.page = page

    def click_element(self, selector):
        self.page.click(selector)

    def type_text(self, selector, text):
        self.page.locator(selector).press_sequentially(text)

    def get_url(self):
        return self.page.url()

    def navigate(self, url):
        self.page.goto(url)

    def click_and_wait_download(self, selector, timeout=30000):
        with self.page.expect_download(timeout=timeout) as download_info:
            self.page.click(selector)
        download = download_info.value
        return download.path()

    def wait_for_url(self, url):
        self.page.wait_for_url(f"**{url}")

    def click_element_with_text(self, loc, text):
        self.page.locator(loc).filter(has_text=text).click()

    def wait_for_element_visible(self, loc):
        self.page.locator(loc).wait_for(state='visible')