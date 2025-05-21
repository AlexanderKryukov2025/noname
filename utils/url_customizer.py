from urllib.parse import urlencode
from datetime import datetime, timedelta

class UrlBuilder:
    def build_event_url(
        self,
        base_url="https://.../event?",
        date_from=None,
        date_to=None,
        date_from_hour=None,
        date_from_minute=None,
        date_to_hour=None,
        date_to_minute=None,
        filter_set=None,
        client_id=None,
        driver_uid=None,
        event_id=None,
        external_driver_id=None,
        device_type=None,
        type_list=None,
        data=None
    ):
        params = {}

        # Объединённое добавление параметров
        for key, value in [
            ('date_from', date_from),
            ('date_to', date_to),
            ('date_from_hour', date_from_hour),
            ('date_from_minute', date_from_minute),
            ('date_to_hour', date_to_hour),
            ('date_to_minute', date_to_minute),
            ('filter_set', filter_set),
            ('client_id', client_id),
            ('driver_uid', driver_uid),
            ('event_id', event_id),
            ('external_driver_id', external_driver_id),
            ('device_type', device_type),
            ('data', data)
        ]:
            if value is not None:
                params[key] = value

        # Обработка type_list
        if type_list:
            params['type[]'] = type_list

        # Кодируем параметры
        query_string = urlencode(params, doseq=True, safe='+')
        return f"{base_url}?{query_string}"

class UrlParams:
    def __init__(self, base_url, builder):
        self._base_url = base_url
        self._builder = builder
        self._params = {}
        self._type_list = []

    def set_params(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                if key == 'type_list':
                    self._type_list.extend(value)
                else:
                    self._params[key] = value
        return self

    def build(self):
        return self._builder.build_event_url(
            base_url=self._base_url,
            **self._params,
            type_list=self._type_list
        )

class UrlProvider:
    def __init__(self, default_url):
        self._default_url = default_url
        self._builder = UrlBuilder()

    def _get_date_range(self, start_date: datetime, end_date: datetime):
        date_from = '+' + start_date.strftime("%d.%m.%Y") + '+'
        date_to = '+' + end_date.strftime("%d.%m.%Y") + '+'
        return {
            'date_from': date_from,
            'date_to': date_to,
            'date_from_hour': 00,
            'date_from_minute': 00,
            'date_to_hour': 23,
            'date_to_minute': 59,
        }

    def build(self, url=None):
        if url:
            self._current_url = url
        return self._current_url

    def _build_params_for_range(self, **kwargs):
        # Общий метод для сборки параметров по диапазону дат
        return UrlParams(self._default_url, self._builder).set_params(
            filter_set=1,
            **kwargs,
            data=1
        )

    def get_today(self):
        today_date = datetime.now().date()
        start = datetime.combine(today_date, datetime.min.time())
        end = datetime.combine(today_date, datetime.max.time())
        range_params = self._get_date_range(start, end)
        return self._build_params_for_range(**range_params)

    def get_yesterday(self):
        yesterday = datetime.now() - timedelta(days=1)
        start = datetime.combine(yesterday.date(), datetime.min.time())
        end = datetime.combine(yesterday.date(), datetime.max.time())
        range_params = self._get_date_range(start, end)
        return self._build_params_for_range(**range_params)

    def recent_events(self):
        end = datetime.now()
        start = end - timedelta(days=1)
        range_params = self._get_date_range(start, end)
        start_hour = str(int(start.strftime("%H")))
        start_minute = str(int(start.strftime("%M")))
        end_hour = end.strftime("%H")
        end_minute = str(int(end.strftime("%M")))

        for key in ['date_from_hour', 'date_from_minute', 'date_to_hour', 'date_to_minute']:
            range_params.pop(key, None)

        return self._build_params_for_range(
            **range_params,
            date_from_hour=start_hour,
            date_from_minute=start_minute,
            date_to_hour=end_hour,
            date_to_minute=end_minute
        )

    def get_day_before_yesterday(self):
        end = datetime.now() - timedelta(days=2)
        start = end
        range_params = self._get_date_range(start, end)
        return self._build_params_for_range(**range_params)

    def get_current_week(self):
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())  # Понедельник
        start = datetime.combine(start_of_week.date(), datetime.min.time())
        end = datetime.now()
        range_params = self._get_date_range(start, end)
        return self._build_params_for_range(**range_params)

    def get_previous_week(self):
        today = datetime.now()
        start_of_current_week = today - timedelta(days=today.weekday())
        start_of_prev_week = start_of_current_week - timedelta(days=7)
        end_of_prev_week = start_of_current_week - timedelta(days=1)
        start = datetime.combine(start_of_prev_week.date(), datetime.min.time())
        end = datetime.combine(end_of_prev_week.date(), datetime.max.time())
        range_params = self._get_date_range(start, end)
        return self._build_params_for_range(**range_params)

    def get_current_month(self):
        today = datetime.now()
        start = today.replace(day=1)
        end = datetime.now()
        range_params = self._get_date_range(start, end)
        return self._build_params_for_range(**range_params)

    def get_past_month(self):
        today = datetime.now()
        first_day_current_month = today.replace(day=1)
        last_day_prev_month = first_day_current_month - timedelta(days=1)
        start_prev_month = last_day_prev_month.replace(day=1)
        end_prev_month = last_day_prev_month
        range_params = self._get_date_range(start_prev_month, end_prev_month)
        return self._build_params_for_range(**range_params)

    def get_current_year(self):
        today = datetime.now()
        start_of_year = today.replace(month=1, day=1)
        end = today
        range_params = self._get_date_range(start_of_year, end)
        return self._build_params_for_range(**range_params)

    def get_past_year(self):
        today = datetime.now()
        start_of_current_year = today.replace(month=1, day=1)
        start_prev_year = start_of_current_year.replace(year=start_of_current_year.year - 1)
        end_prev_year = start_of_current_year - timedelta(days=1)
        range_params = self._get_date_range(start_prev_year, end_prev_year)
        return self._build_params_for_range(**range_params)

# Пример использования
default_url = "https://example/event"
url_provider = UrlProvider(default_url)

# # Получить текущий неделя
# url = url_provider.get_current_week().set_params(
#     type_list=[17, 40, 26, 27, 46, 38, 4, 28, 25],
#     data=2
# ).build()
#
# print(url)

print("Сутки:", url_provider.recent_events().set_params(type_list=[17, 40], data=2).build())
print("Сегодня:", url_provider.get_today().set_params(type_list=[17, 40], data=2).build())
print("Вчера:", url_provider.get_yesterday().set_params(type_list=[17], data=1).build())
print("Текущая неделя:", url_provider.get_current_week().set_params(type_list=[26]).build())
print("Прошлая неделя:", url_provider.get_previous_week().set_params(type_list=[27]).build())
print("Текущий месяц:", url_provider.get_current_month().set_params(type_list=[46]).build())
print("Прошлый месяц:", url_provider.get_past_month().set_params(type_list=[38]).build())
print("Текущий год:", url_provider.get_current_year().set_params(type_list=[4]).build())
print("Прошлый год:", url_provider.get_past_year().set_params(type_list=[28]).build())
