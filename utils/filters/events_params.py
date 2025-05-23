from datetime import datetime, timedelta

class EventsParamsBuilder:
    def __init__(self):
        self.params = {
            "page": 1,
            "filter[client_id]": None,
            "filter[org_struct_lvl1_id]": None,
            "filter[org_struct_lvl2_id]": None,
            "filter[geofence_id]": None,
            "filter[side_number]": None,
            "filter[vehicle_id]": None,
            "filter[device_id]": None,
            "filter[device_type]": None,
            "filter[date_from]": None,
            "filter[date_to]": None,
            "filter[type]": None,
            "filter[driver_uid]": None,
            "filter[external_driver_id]": None,
            "filter[operator_id]": None,
            "filter[verification_status]": None,
            "filter[speed_not_null]": None,
            "filter[event_id]": None,
            "filter[event_uid]": None
        }

    def set_param(self, key, value):
        # Проверка, является ли ключ списком для специальных обработок
        if isinstance(value, list):
            # Преобразуем каждый элемент списка в отдельный параметр с индексом
            for idx, item in enumerate(value):
                param_key = f"{key}[{idx}]"
                self.params[param_key] = item
        else:
            # Стандартная установка
            if key in self.params:
                self.params[key] = value
        return self

    def set_params(self, params_dict):
        for key, value in params_dict.items():
            self.set_param(key, value)
        return self

    def build(self):
        # Убираем параметры со значением None
        filtered_params = {k: v for k, v in self.params.items() if v is not None}
        return filtered_params

# Класс для работы с датами
class EventsDateRangeMethods:
    def _get_date_range(self, start_date: datetime, end_date: datetime):
        date_from = start_date.isoformat(timespec='milliseconds') + 'Z'
        date_to = end_date.isoformat(timespec='milliseconds') + 'Z'
        return {
            "filter[date_from]": date_from,
            "filter[date_to]": date_to
        }

    def get_today(self):
        today = datetime.now().date()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        return self._set_date_range(start, end)

    def get_yesterday(self):
        yesterday = datetime.now() - timedelta(days=1)
        start = datetime.combine(yesterday.date(), datetime.min.time())
        end = datetime.combine(yesterday.date(), datetime.max.time())
        return self._set_date_range(start, end)

    def recent_events(self):
        end = datetime.now()
        start = end - timedelta(days=1)
        return self._set_date_range(start, end)

    def get_day_before_yesterday(self):
        end = datetime.now() - timedelta(days=2)
        start = end
        return self._set_date_range(start, end)

    def get_current_week(self):
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        start = datetime.combine(start_of_week.date(), datetime.min.time())
        end = datetime.now()
        return self._set_date_range(start, end)

    def get_previous_week(self):
        today = datetime.now()
        start_of_current_week = today - timedelta(days=today.weekday())
        start_of_prev_week = start_of_current_week - timedelta(days=7)
        end_of_prev_week = start_of_current_week - timedelta(days=1)
        start = datetime.combine(start_of_prev_week.date(), datetime.min.time())
        end = datetime.combine(end_of_prev_week.date(), datetime.max.time())
        return self._set_date_range(start, end)

    def get_current_month(self):
        today = datetime.now()
        start = today.replace(day=1)
        end = datetime.now()
        return self._set_date_range(start, end)

    def get_past_month(self):
        today = datetime.now()
        first_day_current_month = today.replace(day=1)
        last_day_prev_month = first_day_current_month - timedelta(days=1)
        start_prev_month = last_day_prev_month.replace(day=1)
        end_prev_month = last_day_prev_month
        return self._set_date_range(start_prev_month, end_prev_month)

    def get_current_year(self):
        today = datetime.now()
        start_of_year = today.replace(month=1, day=1)
        end = datetime.now()
        return self._set_date_range(start_of_year, end)

    def get_past_year(self):
        today = datetime.now()
        start_of_current_year = today.replace(month=1, day=1)
        start_prev_year = start_of_current_year.replace(year=start_of_current_year.year - 1)
        end_prev_year = start_of_current_year - timedelta(days=1)
        return self._set_date_range(start_prev_year, end_prev_year)

    def _set_date_range(self, start, end):
        self.set_params(self._get_date_range(start, end))
        return self

# Класс для фильтров, наследует от builder и методов для дат
class EventsParams(EventsParamsBuilder, EventsDateRangeMethods):
    def __init__(self):
        super().__init__()
        # Инициализация методов для дат
        # Можно оставить пустым, так как методы уже есть
        # Или дополнительно можно инициализировать, если нужно

    # Методы для установки фильтров
    def set_page_num(self, page_num):
        return self.set_param("page", page_num)

    def set_date_from(self, date_from):
        return self.set_param("filter[date_from]", date_from)

    def set_date_to(self, date_to):
        return self.set_param("filter[date_to]", date_to)

    def set_client_id(self, client_id):
        return self.set_param("filter[client_id]", client_id)

    def set_org_struct_lvl1_id(self, id):
        return self.set_param("filter[org_struct_lvl1_id]", id)

    def set_org_struct_lvl2_id(self, id):
        return self.set_param("filter[org_struct_lvl2_id]", id)

    def set_geofence_id(self, geofence_id):
        return self.set_param("filter[geofence_id]", geofence_id)

    def set_side_number(self, side_number):
        return self.set_param("filter[side_number]", side_number)

    def set_vehicle_id(self, vehicle_id):
        return self.set_param("filter[vehicle_id]", vehicle_id)

    def set_device_id(self, device_id):
        return self.set_param("filter[device_id]", device_id)

    def set_device_type(self, device_type):
        return self.set_param("filter[device_type]", device_type)

    def set_type(self, event_type):
        return self.set_param("filter[type]", event_type)

    def set_driver_uid(self, driver_uid):
        return self.set_param("filter[driver_uid]", driver_uid)

    def set_external_driver_id(self, external_driver_id):
        return self.set_param("filter[external_driver_id]", external_driver_id)

    def set_operator_id(self, operator_id):
        return self.set_param("filter[operator_id]", operator_id)

    def set_verification_status(self, status):
        return self.set_param("filter[verification_status]", status)

    def set_speed_not_null(self, speed_not_null=True):
        return self.set_param("filter[speed_not_null]", speed_not_null)

    def set_event_id(self, event_id):
        return self.set_param("filter[event_id]", event_id)

    def set_event_uid(self, event_uid):
        return self.set_param("filter[event_uid]", event_uid)

# # # Примеры вызова в одну строку
# # print("Сутки:", EventsParams().recent_events().set_params({"filter[type]": [17, 40], "filter[external_driver_id]": 2}).build())
# # print("Сегодня:", EventsParams().get_today().set_params({"filter[type]": [17, 40], "filter[external_driver_id]": 2}).build())
# # print("Вчера:", EventsParams().get_yesterday().set_params({"filter[type]": [17], "filter[external_driver_id]": 1}).build())
# # print("Текущая неделя:", EventsParams().get_current_week().set_params({"filter[type]": [26]}).build())
# # print("Прошлая неделя:", EventsParams().get_previous_week().set_params({"filter[type]": [27]}).build())
# # print("Текущий месяц:", EventsParams().get_current_month().set_params({"filter[type]": [46]}).build())
# # print("Прошлый месяц:", EventsParams().get_past_month().set_params({"filter[type]": [38]}).build())
# # print("Текущий год:", EventsParams().get_current_year().set_params({"filter[type]": [4]}).build())
# # print("Прошлый год:", EventsParams().get_past_year().set_params({"filter[type]": [28]}).build())
