import os
import csv
from datetime import datetime

# current_dir = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT = os.path.abspath(os.path.join(current_dir, '..'))
# report = EventReport(PROJECT_ROOT).build_report(data)
# print(f"Отчет сохранен по пути: {report.file_path}")

import os
import csv
from datetime import datetime

class EventReport:
    def __init__(self, report_dir):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'event_report_{timestamp}.csv'
        self.file_path = os.path.join(report_dir, filename)

    def build_report(self, data_list, sort_columns=None, sort_by=None, sort_order='asc'):
        headers = [
            "Id",
            "Дата события",
            "Время события",
            "Организационная структура",
            "Организационная структура",
            "Борт.№",
            "Событие",
            "Статус",
            "Название устройства",
            "Регистрационный номер",
            "Скорость",
            "Координаты",
            "Фото",
            "Видео",
            "Лог",
            "Водитель",
            "VIN код"
        ]

        # Предварительная обработка данных для сортировки
        def get_sort_key(item):
            key = []
            if sort_columns:
                for col in sort_columns:
                    key.append(self._get_field_value(item, col))
            elif sort_by:
                key.append(self._get_field_value(item, sort_by))
            else:
                # Если сортировка не указана, используем id
                key.append(item.get('id', ''))
            return tuple(key)

        # Получение значения поля для сортировки по названию колонки
        def get_field_value(item, column_name):
            # Названия колонок совпадают с заголовками
            if column_name == "Id":
                return item.get('id', '')
            elif column_name == "Дата события":
                created_at = item.get('created_at', '')
                dt_obj = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S') if created_at else None
                return dt_obj.strftime('%Y-%m-%d') if dt_obj else ''
            elif column_name == "Время события":
                created_at = item.get('created_at', '')
                dt_obj = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S') if created_at else None
                return dt_obj.strftime('%H:%M:%S') if dt_obj else ''
            elif column_name == "Организационная структура":
                return item.get('org_struct_lvl1', {}).get('name', '')
            elif column_name == "Борт.№":
                vehicle = item.get('vehicle', {})
                return vehicle.get('registration_number', '')
            elif column_name == "Событие":
                return item.get('type', '')
            elif column_name == "Статус":
                return item.get('status', {}).get('title', '')
            elif column_name == "Название устройства":
                return item.get('device', {}).get('name', '')
            elif column_name == "Регистрационный номер":
                vehicle = item.get('vehicle', {})
                return vehicle.get('registration_number', '')
            elif column_name == "Скорость":
                return item.get('speed', '')
            elif column_name == "Координаты":
                latitude = item.get('latitude', '')
                longitude = item.get('longitude', '')
                return f"{latitude}, {longitude}"
            elif column_name == "Фото":
                return item.get('photo', '')
            elif column_name == "Видео":
                videos = item.get('video', [])
                video_urls = [v.get('url', '') for v in videos]
                return ', '.join(video_urls)
            elif column_name == "Лог":
                return ''
            elif column_name == "Водитель":
                return item.get('driver', {}).get('name', '')
            elif column_name == "VIN код":
                vehicle = item.get('vehicle', {})
                return vehicle.get('vin', '')
            else:
                return ''

        # Обертка для получения значения поля по названию колонки
        self._get_field_value = get_field_value

        # Сортировка данных
        if (sort_columns or sort_by):
            reverse = (sort_order == 'desc')
            data_list = sorted(data_list, key=get_sort_key, reverse=reverse)

        with open(self.file_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(headers)

            for item in data_list:
                try:
                    # Идентификатор события
                    event_id = item.get('id', '')

                    # Дата и время события
                    created_at = item.get('created_at', '')
                    dt_obj = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S') if created_at else None
                    date_event = dt_obj.strftime('%Y-%m-%d') if dt_obj else ''
                    time_event = dt_obj.strftime('%H:%M:%S') if dt_obj else ''

                    # Организационная структура (два раза, как в колонках)
                    org_struct_lvl1_name = item.get('org_struct_lvl1', {}).get('name', '')
                    org_struct_lvl2_name = ''  # В примере нет данных, можно оставить пустым или дополнительно брать, если есть

                    # Бортовой номер
                    vehicle = item.get('vehicle', {})
                    registration_number = vehicle.get('registration_number', '')

                    # Событие
                    event_type = item.get('type', '')

                    # Статус
                    status = item.get('status', {}).get('title', '')

                    # Название устройства
                    device_name = item.get('device', {}).get('name', '')

                    # Регистрационный номер (тот же, что и бортовой)
                    reg_number = registration_number

                    # Скорость
                    speed = item.get('speed', '')

                    # Координаты
                    latitude = item.get('latitude', '')
                    longitude = item.get('longitude', '')
                    coordinates = f"{latitude}, {longitude}"

                    # Фото
                    photo_url = item.get('photo', '')

                    # Видео (объединяем все ссылки через запятую)
                    videos = item.get('video', [])
                    video_urls = [v.get('url', '') for v in videos]
                    video_str = ', '.join(video_urls)

                    # Лог — можно оставить пустым или добавить какую-то информацию
                    log = ''

                    # Водитель
                    driver_name = item.get('driver', {}).get('name', '')

                    # VIN код — в данном случае использую VIN из vehicle, или можно оставить пустым
                    vin_code = item.get('vehicle', {}).get('vin', '')

                    row = [
                        event_id,
                        date_event,
                        time_event,
                        org_struct_lvl1_name,
                        org_struct_lvl2_name,
                        registration_number,
                        event_type,
                        status,
                        device_name,
                        reg_number,
                        speed,
                        coordinates,
                        photo_url,
                        video_str,
                        log,
                        driver_name,
                        vin_code
                    ]

                    writer.writerow(row)

                except Exception as e:
                    print(f"Ошибка при обработке записи {item.get('id', '')}: {e}")

# Пример использования:
# report = EventReport('/path/to/save')
# data_list = [...]  # Ваш список данных

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

# class EventReport:
#     def __init__(self, report_dir):
#         self.report_dir = report_dir
#         os.makedirs(report_dir, exist_ok=True)
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         filename = f'event_report_{timestamp}.csv'
#         self.file_path = os.path.join(report_dir, filename)
#
#     def build_report(self, data_list):
#         headers = [
#             "Id",
#             "Дата события",
#             "Время события",
#             "Организационная структура",
#             "Организационная структура",
#             "Борт.№",
#             "Событие",
#             "Статус",
#             "Название устройства",
#             "Регистрационный номер",
#             "Скорость",
#             "Координаты",
#             "Фото",
#             "Видео",
#             "Лог",
#             "Водитель",
#             "VIN код"
#         ]
#
#         with open(self.file_path, mode='w', encoding='utf-8', newline='') as file:
#             writer = csv.writer(file, delimiter=';')
#             writer.writerow(headers)
#
#             for item in data_list:
#                 try:
#                     # Идентификатор события
#                     event_id = item.get('id', '')
#
#                     # Дата и время события
#                     created_at = item.get('created_at', '')
#                     dt_obj = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S') if created_at else None
#                     date_event = dt_obj.strftime('%Y-%m-%d') if dt_obj else ''
#                     time_event = dt_obj.strftime('%H:%M:%S') if dt_obj else ''
#
#                     # Организационная структура (два раза, как в колонках)
#                     org_struct_lvl1_name = item.get('org_struct_lvl1', {}).get('name', '')
#                     org_struct_lvl2_name = ''  # В примере нет данных, оставим пустым или можно дополнительно брать, если есть
#
#                     # Бортовой номер
#                     vehicle = item.get('vehicle', {})
#                     registration_number = vehicle.get('registration_number', '')
#
#                     # Событие
#                     event_type = item.get('type', '')
#
#                     # Статус
#                     status = item.get('status', {}).get('title', '')
#
#                     # Название устройства
#                     device_name = item.get('device', {}).get('name', '')
#
#                     # Регистрационный номер (тот же, что и бортовой)
#                     reg_number = registration_number
#
#                     # Скорость
#                     speed = item.get('speed', '')
#
#                     # Координаты
#                     latitude = item.get('latitude', '')
#                     longitude = item.get('longitude', '')
#                     coordinates = f"{latitude}, {longitude}"
#
#                     # Фото
#                     photo_url = item.get('photo', '')
#
#                     # Видео (объединяем все ссылки через запятую)
#                     videos = item.get('video', [])
#                     video_urls = [v.get('url', '') for v in videos]
#                     video_str = ', '.join(video_urls)
#
#                     # Лог — можно оставить пустым или добавить какую-то информацию
#                     log = ''
#
#                     # Водитель
#                     driver_name = item.get('driver', {}).get('name', '')
#
#                     # VIN код — в данном случае использую регистрационный номер, либо можно оставить пустым
#                     vin_code = reg_number
#
#                     row = [
#                         event_id,
#                         date_event,
#                         time_event,
#                         org_struct_lvl1_name,
#                         org_struct_lvl2_name,
#                         registration_number,
#                         event_type,
#                         status,
#                         device_name,
#                         reg_number,
#                         speed,
#                         coordinates,
#                         photo_url,
#                         video_str,
#                         log,
#                         driver_name,
#                         vin_code
#                     ]
#
#                     writer.writerow(row)
#
#                 except Exception as e:
#                     print(f"Ошибка при обработке записи {item.get('id', '')}: {e}")
