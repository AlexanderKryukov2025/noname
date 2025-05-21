import allure
import pytest

from pages.login_page import LoginPage, LoginPageAsync
from pages.main_page import MainPage, MainPageAsync
from pages.device_page import DevicePage, DevicePageAsync
from playwright.async_api import async_playwright
from utils.logger import setup_logging
from settings import STG


@allure.feature("Авторизация и навигация")
@allure.story("Пользовательский сценарий")
@allure.tag("FRONT")
def test_login_and_navigate(page):
    login_page = LoginPage(page)
    main_page = MainPage(page)
    device_page = DevicePage(page)
    login_page.open_page(STG.ANTISLEEP['url'])
    login_page.verify_language()
    login_page.enter_email(STG.ANTISLEEP['login'])
    login_page.enter_password(STG.ANTISLEEP['password'])
    login_page.click_submit()
    main_page.check_landing()
    main_page.navigate_to_devices()
    device_page.check_landing()
    device_page.switch_columns()
    device_page.close_popup()
    device_page.press_export_excel()
    device_page.wait_notification()
    device_page.press_download()


@allure.feature("Авторизация и навигация")
@allure.story("Пользовательский сценарий")
@allure.tag("FRONT")
@pytest.mark.asyncio
async def test_login_and_navigate_async():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()

        login_page = LoginPageAsync(page)
        main_page = MainPageAsync(page)
        device_page = DevicePageAsync(page)

        await login_page.open_page(STG.ANTISLEEP['url'])
        await login_page.verify_language()
        await login_page.enter_email(STG.ANTISLEEP['login'])
        await login_page.enter_password(STG.ANTISLEEP['password'])
        await login_page.click_submit()
        await main_page.check_landing()
        await main_page.navigate_to_devices()
        await device_page.check_landing()
        await device_page.switch_columns()
        await device_page.close_popup()
        await device_page.press_export_excel()
        await device_page.wait_notification()
        await device_page.press_download()
