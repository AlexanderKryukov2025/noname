import allure

from pages.sync_page import SyncPage
from pages.async_page import AsyncPage
from locators import Locators


class MainPage(SyncPage):

    def __init__(self, page, loc=Locators()):
        super().__init__(page)
        self.main_loc = loc("main")

    @allure.step("Проверка загрузки главной страницы")
    def check_landing(self):
        self.wait_for_element_visible(self.main_loc['logout_btn'])

    @allure.step("Навигация к устройствам")
    def navigate_to_devices(self):
        self.click_element_with_text(self.main_loc['tab_links'], self.locale.get('devices'))


class MainPageAsync(AsyncPage):
    def __init__(self, page, loc=Locators()):
        super().__init__(page)
        self.main_loc = loc("main")

    @allure.step("Проверка загрузки главной страницы")
    async def check_landing(self):
        await self.wait_for_element_visible(self.main_loc['logout_btn'])

    @allure.step("Навигация к устройствам")
    async def navigate_to_devices(self):
        await self.click_element_with_text(self.main_loc['tab_links'], self.locale.get('devices'))

    @allure.step("Проверка локализации")
    async def check_lang(self):
        return await self.get_element_text(self.main_loc['lang'])
