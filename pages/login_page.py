import allure
import asyncio

from pages.sync_page import SyncPage
from pages.async_page import AsyncPage
from locators import Locators


class LoginPage(SyncPage):

    def __init__(self, page, loc=Locators()):
        super().__init__(page)
        self.login_loc = loc("login")

    @allure.step("Открыть страницу входа")
    def open_page(self, url):
        self.navigate(url)
        self.page.wait_for_load_state('load')

    @allure.step("Ввести email")
    def enter_email(self, email):
        self.type_text(self.login_loc['email_input'], email)

    @allure.step("Ввести пароль")
    def enter_password(self, password):
        self.type_text(self.login_loc['password_input'], password)

    @allure.step("Нажать кнопку 'Вход'")
    def click_submit(self):
        self.click_element(self.login_loc['submit_btn'])


class LoginPageAsync(AsyncPage):
    def __init__(self, page, loc=Locators()):
        super().__init__(page)
        self.login_loc = loc("login")

    @allure.step("Открыть страницу входа")
    async def open_page(self, url):
        await self.navigate(url)

    @allure.step("Ввести email")
    async def enter_email(self, email):
        await self.type_text(self.login_loc["email_input"], email)

    @allure.step("Ввести пароль")
    async def enter_password(self, password):
        await self.type_text(self.login_loc["password_input"], password)

    @allure.step("Нажать кнопку 'Вход'")
    async def click_submit(self):
        await self.click_element(self.login_loc["submit_btn"])
