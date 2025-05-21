import threading
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.device_page import DevicePage
from settings import STG
from utils.url_customizer import UrlProvider

PILLI_EVENT_TYPES = [17, 61, 40, 26, 27, 46, 38, 4, 28, 25]
MGT_EVENT_TYPES = [17, 40, 26, 27, 46, 38, 4, 28, 2]

def run_browser_session(url, login, password):
    # Эта функция запускается в отдельном потоке
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Создаем классы страниц
        login_page = LoginPage(page)
        main_page = MainPage(page)
        device_page = DevicePage(page)
        # url_modified = UrlProvider(url+'/event').recent_events().set_params(type_list=PILLI_EVENT_TYPES,).build()

        # Выполняем последовательность действий синхронно
        run_pages_sequence(url, login, password, login_page, main_page, device_page)


def run_pages_sequence(url, login, password, login_page, main_page, device_page):
    login_page.open_page(url) # TODO входить используя куки (как формировать куки?)
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
        (STG.MGT['url'], STG.MGT['login'], STG.MGT['password']),
        (STG.PILLIGRIMM['url'], STG.PILLIGRIMM['login'], STG.PILLIGRIMM['password'])
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
