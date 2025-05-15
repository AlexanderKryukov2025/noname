import allure

from .base_page import BasePage
from locators import Locators


class MainPage(BasePage):

    def __init__(self, page, loc=Locators()):
        super().__init__(page)
        self.page = page
        self.login_loc = loc("main")

    @allure.step("Проверить загрузку главной страницы")
    def check_landing(self):
        self.wait_for_url('/client-113')

    @allure.step("Навигация к устройствам")
    def navigate_to_devices(self):
        self.click_element_with_text(self.login_loc['tab_links'], 'Devices')
