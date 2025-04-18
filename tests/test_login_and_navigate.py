import allure
from settings import STG
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.device_page import DevicePage


@allure.feature("Авторизация и навигация")
@allure.story("Пользовательский сценарий")
def test_login_and_navigate(driver):
    login_page = LoginPage(driver)
    main_page = MainPage(driver)
    device_page = DevicePage(driver)
    devices_item = main_page.menu_items['devices']

    with allure.step("Открыть страницу входа"):
        login_page.open_page(STG.ANTISLEEP['host'])

    with allure.step("Ввести email"):
        login_page.enter_email(STG.ANTISLEEP['login'])

    with allure.step("Ввести пароль"):
        login_page.enter_password(STG.ANTISLEEP['password'])

    with allure.step("Нажать кнопку 'Вход'"):
        login_page.click_submit()

    with allure.step("Проверить загрузку главной страницы"):
        main_page.check_landing()

    with allure.step("Навигация к устройствам"):
        main_page.navigate_to_devices([devices_item['en'], devices_item['ru']])

    with allure.step("Проверить загрузку страницы устройств"):
        device_page.check_landing()

    with allure.step("Переключить колонки"):
        device_page.switch_columns()

    with allure.step("Закрыть попап"):
        device_page.close_popup()

    with allure.step("Нажать кнопку 'Выгрузить отчет'"):
        device_page.press_export_excel()

    with allure.step("123"):
        asd = 1