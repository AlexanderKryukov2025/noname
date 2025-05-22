import os
import threading
from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.device_page import DevicePage
from settings import STG
from utils.api_payloads.events import EventsParams
from utils.event_report import EventReport

# Константы с типами событий
PILLI_EVENT_TYPES = [17, 61, 40, 26, 27, 46, 38, 4, 28, 25]
MGT_EVENT_TYPES = [17, 40, 26, 27, 46, 38, 4, 28, 2]

# Определение корневой директории проекта
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))


def create_report(login, password, cluster):
    login_params = {"email": login, "password": password}
    params = EventsParams().recent_events().set_params({"page": 1}).build()

    # Получение событий
    token = cluster.login.post_login(params=login_params).decoded_body.get('token')
    response = cluster.events.get_events(token, params=params).decoded_body
    total_events = response.get('total', 0)
    if not total_events:
        print(f"Нет событий")
        return

    total_pages = total_events / 20
    if total_pages % 2 != 0:
        total_pages = int(total_pages)

    data = []
    # Получение данных по страницам
    for page_num in range(1, total_pages + 1):
        params['page'] = page_num
        response = cluster.events.get_events(token, params=params).decoded_body
        data.extend(response.get('data', []))

    # Генерация отчета
    EventReport(PROJECT_ROOT).build_report(
        data,
        sort_columns=["Событие", "Статус"],
        sort_order='asc'
    )



# Сортировка по двум колонкам
# report.build_report(
#     data_list,
#     sort_columns=["Дата события", "Время события"],
#     sort_order='asc'
# )

# Или сортировка по одной колонке
# report.build_report(
#     data_list,
#     sort_by="Id",
#     sort_order='desc'
# )

def main(cluster):
    """
    Основная функция запуска потоков для каждой сессии.
    """
    session_params = [
        # (STG.MGT['url'], STG.MGT['login'], STG.MGT['password']),
        (STG.PILLIGRIMM['url'], STG.PILLIGRIMM['login'], STG.PILLIGRIMM['password'])
    ]

    threads = []

    for host, login, pwd in session_params:
        t = threading.Thread(target=create_report, args=(login, pwd, cluster))
        t.start()
        threads.append(t)

    # Ожидание завершения всех потоков
    for t in threads:
        t.join()


def test_main(cluster):
    main(cluster)

# import os
# import threading
#
# from playwright.sync_api import sync_playwright
# from pages.login_page import LoginPage
# from pages.main_page import MainPage
# from pages.device_page import DevicePage
# from settings import STG
# from utils.api_payloads.events_params import EventsParams
# from utils.event_report import EventReport
#
# PILLI_EVENT_TYPES = [17, 61, 40, 26, 27, 46, 38, 4, 28, 25]
# MGT_EVENT_TYPES = [17, 40, 26, 27, 46, 38, 4, 28, 2]
# current_dir = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT = os.path.abspath(os.path.join(current_dir, '..'))
#
#
#
#
# def run_browser_session(url, login, password, cluster):
#         login_params = {"email": login, "password": password}
#         params = EventsParams().recent_events().set_params({"page": 1}).build()
#         token = cluster.login.post_login(params=login_params).decoded_body.get('token')
#         response = cluster.events.get_events(token, params=params).decoded_body
#         total_events = response['total'] # количество событий
#         total_pages = total_events / 20 # количество страниц
#         if total_pages % 2 != 0:
#             total_pages = int(total_pages)
#             total_pages += 1
#
#         data = []
#         for page_num in enumerate(range(total_pages), start=1):
#             params['page'] = page_num
#             response = cluster.events.get_events(token, params=params).decoded_body
#             data.extend(response['data'])
#
#         report = EventReport(PROJECT_ROOT).build_report(data)
#         asd = 1
#
#
#
#         # Выполняем последовательность действий синхронно
#         run_pages_sequence(url, login, password, cluster)
#
#
# def run_pages_sequence(url, login, password, login_page, main_page, device_page, cluster):
#     pass
#
# def main(cluster):
#
#     session_params = [
#         (STG.MGT['url'], STG.MGT['login'], STG.MGT['password']),
#         (STG.PILLIGRIMM['url'], STG.PILLIGRIMM['login'], STG.PILLIGRIMM['password'])
#     ]
#
#
#     threads = []
#
#     for host, login, pwd in session_params:
#         t = threading.Thread(target=run_browser_session, args=(host, login, pwd, cluster))
#         t.start()
#         threads.append(t)
#
#     # Ждем завершения всех потоков
#     for t in threads:
#         t.join()
#
#
# def test_main(cluster):
#     main(cluster)