import allure

from .base_page import BasePage
from pathlib import Path
from locators import Locators


class DevicePage(BasePage):

    def __init__(self, page, loc=Locators()):
        super().__init__(page)
        self.page = page
        self.device_loc = loc("device")

    @allure.step("Проверить загрузку страницы устройств")
    def check_landing(self):
        self.wait_for_url('/device')

    @allure.step("Переключить колонки")
    def switch_columns(self):
        self.click_element(self.device_loc['change_toggle_btn'])

    @allure.step("Закрыть попап")
    def close_popup(self):
        self.click_element(self.device_loc['popup_close_btn'])

    @allure.step("Нажать кнопку 'Выгрузить отчет'")
    def press_export_excel(self):
        self.click_element(self.device_loc['export_excel_btn'])

    @allure.step("Ожидание уведомления о готовности отчета")
    def wait_notification(self):
        self.wait_for_element_visible(self.device_loc['notification_modal'])

    @allure.step("Скачать файл")
    def press_download(self):
        path = self.click_and_wait_download(self.device_loc['created_file_csv'])
        assert Path(path).is_file(), 'File not found'
