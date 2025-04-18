from selenium.webdriver.common.by import By
from helpers.main import wait_until_present, wait_until_visible, wait_text_in_curr_url
from helpers.browser_logs import BrowserLogs

class DevicePage:
    def __init__(self, driver):
        self.driver = driver
        self.change_toggle_btn = (By.CSS_SELECTOR, '.justify-content-end button')
        self.popup_close_btn = (By.CSS_SELECTOR, '.modal-dialog button.close')
        self.export_excel_btn = (By.CSS_SELECTOR, '.card button[name="export"]')
        self.created_file_csv = (By.CSS_SELECTOR, '.modal-dialog .modal-body a')

    def check_landing(self):
        wait_text_in_curr_url(self.driver, '/device', True)

    def switch_columns(self):
        wait_until_present(self.driver, self.change_toggle_btn).click()

    def close_popup(self):
        wait_until_visible(self.driver, self.popup_close_btn).click()

    def press_export_excel(self):
        wait_until_present(self.driver, self.export_excel_btn).click()

    def wait_notification(self):
        assert BrowserLogs(self.driver, ['Network.webSocketFrameReceived', 'user.notification']).target_event

    def press_download(self):
        wait_until_visible(self.driver, self.created_file_csv).click()
        assert BrowserLogs(self.driver, ['Page.downloadProgress', '"state":"completed"']).target_event

