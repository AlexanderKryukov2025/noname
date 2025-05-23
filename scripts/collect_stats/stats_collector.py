import os
import threading

from datetime import datetime
from utils.filters.events_params import EventsParams
from utils.filters.devices_params import DevicesParams
from utils.event_report import EventReport
from settings import STG

PILI_EVENT_TYPES = [17, 61, 40, 26, 27, 46, 38, 4, 28, 25]
PILI_CLIENTS = []
PILI_DEVICES = []
MGT_EVENT_TYPES = [17, 40, 26, 27, 46, 38, 4, 28, 2]
MGT_CLIENTS = []
MGT_DEVICES = []

# Определение корневой директории проекта
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))


def create_report(login, password, cluster):
    login_params = {"email": login, "password": password}
    token = cluster.login.post_login(params=login_params).decoded_body.get('token')
    # Получение id клиента Q1
    client_q1 = cluster.user.get_user(token).decoded_body['clients'][0]['id']  # Q1
    # Получение устройств
    params = DevicesParams().set_page_num(1).set_client_id(client_q1).build()
    response = cluster.devices.get_devices(token, params=params).decoded_body
    total_devices = response.get('total', 0)
    if not total_devices:
        print(f"Нет устройств")
        return

    total_pages = total_devices / 15
    if total_pages < 1:
        total_pages = 1

    elif total_pages % 2 != 0:
        total_pages = int(total_pages)

    data = []
    # Получение событий по страницам
    for page_num in range(1, total_pages + 1):
        params['page'] = page_num
        response = cluster.devices.get_devices(token, params=params).decoded_body
        data.extend(response.get('data', []))

    # Получение событий
    params = EventsParams().recent_events().build()
    params = EventsParams().recent_events().set_page_num(1).build()

    target_devices = []
    for device in data:
        # Задаем диапазон дат
        start_str = params['filter[date_from]']
        end_str = params['filter[date_to]']

        # Время события
        event_str = device['last_ping']

        # Функция для парсинга строк в объекты datetime
        def parse_datetime(dt_str):
            return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Парсим строки
        start_dt = parse_datetime(start_str)
        end_dt = parse_datetime(end_str)
        event_dt = parse_datetime(event_str)

        # Проверяем, входит ли событие в диапазон
        if start_dt <= event_dt <= end_dt:
            target_devices.append(device)

    start_str = params['filter[date_from]']
    end_str = params['filter[date_to]']
    device_ids = [device['id'] for device in target_devices]
    params = EventsParams().set_date_from(start_str).set_date_to(end_str).set_device_id(device_ids).build()

    response = cluster.events.get_events(token, params=params).decoded_body

    total_events = response.get('total', 0)
    if not total_events:
        print(f"Нет событий")
        return

    total_pages = total_events / 20
    if total_pages < 1:
        total_pages = 1

    elif total_pages % 2 != 0:
        total_pages = int(total_pages)

    data = []
    # Получение событий по страницам
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
# from utils.filters.events_params import EventsParams
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

# import os
# import threading
#
# from settings import STG
# from utils.filters.events import EventsParams
# from utils.filters.devices import DevicesParams
# from utils.event_report import EventReport
#
# PILI_EVENT_TYPES = [17, 61, 40, 26, 27, 46, 38, 4, 28, 25]
# PILI_CLIENTS = []
# PILI_DEVICES = []
# MGT_EVENT_TYPES = [17, 40, 26, 27, 46, 38, 4, 28, 2]
# MGT_CLIENTS = []
# MGT_DEVICES = []
#
#
# # Определение корневой директории проекта
# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
#
#
# def create_report(login, password, cluster):
#     login_params = {"email": login, "password": password}
#     token = cluster.login.post_login(params=login_params).decoded_body.get('token')
#     # Получение id клиента Q1
#     client_q1 = cluster.user.get_user(token).decoded_body['clients'][0]['id'] # Q1
#     # Получение устройств
#     params = DevicesParams().set_page_num(1).set_client_id(client_q1).build()
#     response = cluster.devices.get_devices(token, params=params).decoded_body
#
#     # Получение событий
#     params = EventsParams().recent_events().set_page_num(1).build()
#     response = cluster.events.get_events(token, params=params).decoded_body
#     total_events = response.get('total', 0)
#     if not total_events:
#         print(f"Нет событий")
#         return
#
#     total_pages = total_events / 20
#     if total_pages % 2 != 0:
#         total_pages = int(total_pages)
#
#     data = []
#     # Получение событий по страницам
#     for page_num in range(1, total_pages + 1):
#         params['page'] = page_num
#         response = cluster.events.get_events(token, params=params).decoded_body
#         data.extend(response.get('data', []))
#
#     # Генерация отчета
#     EventReport(PROJECT_ROOT).build_report(
#         data,
#         sort_columns=["Событие", "Статус"],
#         sort_order='asc'
#     )
#
#
# def main(cluster):
#     """
#     Основная функция запуска потоков для каждой сессии.
#     """
#     session_params = [
#         # (STG.MGT['url'], STG.MGT['login'], STG.MGT['password']),
#         (STG.PILLIGRIMM['url'], STG.PILLIGRIMM['login'], STG.PILLIGRIMM['password'])
#     ]
#
#     threads = []
#
#     for host, login, pwd in session_params:
#         t = threading.Thread(target=create_report, args=(login, pwd, cluster))
#         t.start()
#         threads.append(t)
#
#     # Ожидание завершения всех потоков
#     for t in threads:
#         t.join()
#
#
# def test_main(cluster):
#     main(cluster)
#
# # import os
# # import threading
# #
# # from playwright.sync_api import sync_playwright
# # from pages.login_page import LoginPage
# # from pages.main_page import MainPage
# # from pages.device_page import DevicePage
# # from settings import STG
# # from utils.filters.events_params import EventsParams
# # from utils.event_report import EventReport
# #
# # PILLI_EVENT_TYPES = [17, 61, 40, 26, 27, 46, 38, 4, 28, 25]
# # MGT_EVENT_TYPES = [17, 40, 26, 27, 46, 38, 4, 28, 2]
# # current_dir = os.path.dirname(os.path.abspath(__file__))
# # PROJECT_ROOT = os.path.abspath(os.path.join(current_dir, '..'))
# #
# #
# #
# #
# # def run_browser_session(url, login, password, cluster):
# #         login_params = {"email": login, "password": password}
# #         params = EventsParams().recent_events().set_params({"page": 1}).build()
# #         token = cluster.login.post_login(params=login_params).decoded_body.get('token')
# #         response = cluster.events.get_events(token, params=params).decoded_body
# #         total_events = response['total'] # количество событий
# #         total_pages = total_events / 20 # количество страниц
# #         if total_pages % 2 != 0:
# #             total_pages = int(total_pages)
# #             total_pages += 1
# #
# #         data = []
# #         for page_num in enumerate(range(total_pages), start=1):
# #             params['page'] = page_num
# #             response = cluster.events.get_events(token, params=params).decoded_body
# #             data.extend(response['data'])
# #
# #         report = EventReport(PROJECT_ROOT).build_report(data)
# #         asd = 1
# #
# #
# #
# #         # Выполняем последовательность действий синхронно
# #         run_pages_sequence(url, login, password, cluster)
# #
# #
# # def run_pages_sequence(url, login, password, login_page, main_page, device_page, cluster):
# #     pass
# #
# # def main(cluster):
# #
# #     session_params = [
# #         (STG.MGT['url'], STG.MGT['login'], STG.MGT['password']),
# #         (STG.PILLIGRIMM['url'], STG.PILLIGRIMM['login'], STG.PILLIGRIMM['password'])
# #     ]
# #
# #
# #     threads = []
# #
# #     for host, login, pwd in session_params:
# #         t = threading.Thread(target=run_browser_session, args=(host, login, pwd, cluster))
# #         t.start()
# #         threads.append(t)
# #
# #     # Ждем завершения всех потоков
# #     for t in threads:
# #         t.join()
# #
# #
# # def test_main(cluster):
# #     main(cluster)