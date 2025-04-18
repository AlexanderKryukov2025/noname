from selenium.webdriver.common.by import By
from helpers.main import wait_until_present


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_input = (By.CSS_SELECTOR, '#email')
        self.password_input = (By.CSS_SELECTOR, '#password')
        self.submit_btn = (By.CSS_SELECTOR, '[type="submit"].btn')

    def open_page(self, url):
        self.driver.get(url)

    def enter_email(self, email):
        wait_until_present(self.driver, self.email_input).send_keys(email)

    def enter_password(self, password):
        wait_until_present(self.driver, self.password_input).send_keys(password)

    def click_submit(self):
        wait_until_present(self.driver, self.submit_btn).click()