import os
import threading

from utils.filters.events_params import EventsParams
from utils.filters.devices_params import DevicesParams
from utils.event_report import EventReport
from settings import STG

# Константы типов событий и клиентов/устройств
PILI_EVENT_TYPES = [17, 61, 40, 26, 27, 46, 38, 4, 28, 25]
PILI_CLIENTS = []
PILI_DEVICES = []
MGT_EVENT_TYPES = [17, 40, 26, 27, 46, 38, 4, 28, 2]
MGT_CLIENTS = []
MGT_DEVICES = []

# Определение корневой директории проекта
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))


def get_total_pages(total_items, items_per_page):
    if total_items == 0:
        return 0
    total_pages = total_items / items_per_page
    total_pages = int(total_pages) if total_pages.is_integer() else int(total_pages) + 1
    return total_pages


def fetch_all_pages(token, base_params, api_request, data_key='data', items_per_page=20):
    response = api_request(token, params=base_params).decoded_body
    total_items = response.get('total', 0)
    total_pages = get_total_pages(total_items, items_per_page)
    all_data = []

    for page in range(1, total_pages + 1):
        params = dict(base_params)
        params['page'] = page
        response = api_request(token, params=params).decoded_body
        all_data.extend(response.get(data_key, []))
    return all_data

def filter_devices_by_date_range(devices, start_dt, end_dt):
    filtered_devices = []

    for device in devices:
        event_dt = device['last_ping']
        if start_dt <= event_dt <= end_dt:
            filtered_devices.append(device)
    return filtered_devices


def create_report(login, password, cluster):
    login_params = {"email": login, "password": password}
    token = cluster.login.post_login(params=login_params).decoded_body.get('token')
    client_q1 = cluster.user.get_user(token).decoded_body['clients'][0]['id']

    # Получение устройств
    device_params = DevicesParams().set_page_num(1).set_client_id(client_q1).build()
    devices = fetch_all_pages(token, device_params, cluster.devices.get_devices, items_per_page=15)

    if not devices:
        print("Нет устройств")
        return

    # Фильтрация устройств по дате
    event_params = EventsParams().recent_events().build()
    date_from = event_params['filter[date_from]']
    date_to = event_params['filter[date_to]']
    target_devices = filter_devices_by_date_range(devices, date_from, date_to)

    if not target_devices:
        print("Нет событий в диапазоне дат")
        return

    # Получение событий
    device_ids = [device['id'] for device in target_devices]
    event_params = EventsParams().set_date_from(date_from).set_date_to(date_to).set_device_id(device_ids).build()
    response = cluster.events.get_events(token, params=event_params).decoded_body

    total_events = response.get('total', 0)
    if not total_events:
        print("Нет событий")
        return

    events = fetch_all_pages(token, event_params, cluster.events.get_events, data_key='data')

    # Генерация отчета
    EventReport(PROJECT_ROOT).build_report(
        events,
        sort_columns=["Статус", "Событие"],
        sort_order='asc'
    )


def main(cluster):
    session_params = [
        # (STG.MGT['url'], STG.MGT['login'], STG.MGT['password']),
        (STG.PILLIGRIMM['url'], STG.PILLIGRIMM['login'], STG.PILLIGRIMM['password'])
    ]

    threads = []

    for host, login, pwd in session_params:
        t = threading.Thread(target=create_report, args=(login, pwd, cluster))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def test_main(cluster):
    main(cluster)
