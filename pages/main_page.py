import allure

from selenium.webdriver.common.by import By
from helpers.main import get_elem_by_text, wait_text_in_curr_url


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.menu_items = {'devices': {'en': 'Devices', 'ru': 'Устройства'}, 'vehicles': {'en': 'Vehicles', 'ru': 'ТС'}}
        self.menu_list = (By.CSS_SELECTOR, 'ul.navbar-nav:not(.navbar-right) li')
        self.devices_btn_ru = (By.LINK_TEXT, 'Устройства')
        self.devices_btn_eng = (By.LINK_TEXT, 'Devices')

    @allure.step("Проверить загрузку главной страницы")
    def check_landing(self):
        wait_text_in_curr_url(self.driver, '/client-113', True)

    @allure.step("Навигация к устройствам")
    def navigate_to_devices(self, item):
        get_elem_by_text(self.driver, self.menu_list, item).click()