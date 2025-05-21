import threading
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.device_page import DevicePage
from settings import STG


def run_browser_session(host, login, password):
    # Эта функция запускается в отдельном потоке
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Создаем классы страниц
        login_page = LoginPage(page)
        main_page = MainPage(page)
        device_page = DevicePage(page)

        # Выполняем последовательность действий синхронно
        run_pages_sequence(host, login, password, login_page, main_page, device_page)


def run_pages_sequence(host, login, password, login_page, main_page, device_page):
    login_page.open_page(host)
    login_page.verify_language()
    login_page.enter_email(login)
    login_page.enter_password(password)
    login_page.click_submit()
    main_page.check_landing()
    main_page.navigate_to_devices()
    device_page.check_landing()
    device_page.switch_columns()
    device_page.close_popup()
    device_page.press_export_excel()
    device_page.wait_notification()
    device_page.press_download()


def main():
    # Данные для двух браузеров
    session_params = [
        (STG.MGT['host'], STG.MGT['login'], STG.MGT['password']),
        (STG.PILLIGRIMM['host'], STG.PILLIGRIMM['login'], STG.PILLIGRIMM['password'])
    ]

    threads = []

    for host, login, pwd in session_params:
        t = threading.Thread(target=run_browser_session, args=(host, login, pwd))
        t.start()
        threads.append(t)

    # Ждем завершения всех потоков
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
