import os
import threading

from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.device_page import DevicePage
from settings import STG
from utils.filters.events_params import EventsParams
from utils.event_report import EventReport

PILLI_EVENT_TYPES = [17, 61, 40, 26, 27, 46, 38, 4, 28, 25]
MGT_EVENT_TYPES = [17, 40, 26, 27, 46, 38, 4, 28, 2]
current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(current_dir, '..'))




def run_browser_session(url, login, password, cluster):
    # Эта функция запускается в отдельном потоке
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Создаем классы страниц
        login_page = LoginPage(page)
        main_page = MainPage(page)
        device_page = DevicePage(page)

        login_params = {
            "email": STG.PILLIGRIMM['login'],
            "password": STG.PILLIGRIMM['password']
        }

        params = EventsParams().recent_events().set_page_num(1).build()
        token = cluster.login.post_login(params=login_params).decoded_body.get('token')
        response = cluster.events.get_events(token, params=params).decoded_body
        total_events = response['total'] # количество событий
        total_pages = total_events / 20 # количество страниц
        if total_pages % 2 != 0:
            total_pages = int(total_pages)
            total_pages += 1

        data = []
        for page_num in enumerate(range(total_pages), start=1):
            params['page'] = page_num
            response = cluster.events.get_events(token, params=params).decoded_body
            data.extend(response['data'])

        report = EventReport(PROJECT_ROOT).build_report(data)
        asd = 1



        # Выполняем последовательность действий синхронно
        run_pages_sequence(url, login, password, login_page, main_page, device_page, cluster)


def run_pages_sequence(url, login, password, login_page, main_page, device_page, cluster):
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


def main(cluster):
    # Данные для двух браузеров
    session_params = [
        (STG.MGT['url'], STG.MGT['login'], STG.MGT['password']),
        (STG.PILLIGRIMM['url'], STG.PILLIGRIMM['login'], STG.PILLIGRIMM['password'])
    ]


    threads = []

    for host, login, pwd in session_params:
        t = threading.Thread(target=run_browser_session, args=(host, login, pwd, cluster))
        t.start()
        threads.append(t)

    # Ждем завершения всех потоков
    for t in threads:
        t.join()


def test_main(cluster):
    main(cluster)