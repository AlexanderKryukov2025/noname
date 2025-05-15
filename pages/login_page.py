import allure

from .base_page import BasePage
from locators import Locators


class LoginPage(BasePage):

    def __init__(self, page, loc=Locators()):
        super().__init__(page)
        self.page = page
        self.login_loc = loc("login")

    @allure.step("Открыть страницу входа")
    def open_page(self, url):
        self.navigate(url)

    @allure.step("Ввести email")
    def enter_email(self, email):
        self.type_text(self.login_loc['email_input'], email)

    @allure.step("Ввести пароль")
    def enter_password(self, password):
        self.type_text(self.login_loc['password_input'], password)

    @allure.step("Нажать кнопку 'Вход'")
    def click_submit(self):
        self.click_element(self.login_loc['submit_btn'])
