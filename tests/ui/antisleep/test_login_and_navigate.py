import allure

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.device_page import DevicePage
from settings import STG


@allure.feature("Авторизация и навигация")
@allure.story("Пользовательский сценарий")
@allure.tag("FRONT")
def test_login_and_navigate(page):
    login_page = LoginPage(page)
    main_page = MainPage(page)
    device_page = DevicePage(page)

    login_page.open_page(STG.ANTISLEEP['host'])
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
