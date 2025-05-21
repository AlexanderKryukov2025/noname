from urllib.parse import urlencode
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pages.sync_page import SyncPage

class UrlBuilder:
    def build_event_url(
        self,
        base_url="https://.../event",
        filter_set=None,
        client_id=None,
        date_from=None,
        date_from_hour=None,
        date_from_minute=None,
        date_to=None,
        date_to_hour=None,
        date_to_minute=None,
        driver_uid=None,
        event_id=None,
        external_driver_id=None,
        device_type=None,
        type_list=None,
        data=None
    ):
        # Создаем словарь параметров
        params = {}

        if filter_set is not None:
            params['filter_set'] = filter_set
        if client_id is not None:
            params['client_id'] = client_id
        if date_from is not None:
            params['date_from'] = date_from
        if date_from_hour is not None:
            params['date_from_hour'] = date_from_hour
        if date_from_minute is not None:
            params['date_from_minute'] = date_from_minute
        if date_to is not None:
            params['date_to'] = date_to
        if date_to_hour is not None:
            params['date_to_hour'] = date_to_hour
        if date_to_minute is not None:
            params['date_to_minute'] = date_to_minute
        if driver_uid is not None:
            params['driver_uid'] = driver_uid
        if event_id is not None:
            params['event_id'] = event_id
        if external_driver_id is not None:
            params['external_driver_id'] = external_driver_id
        if device_type is not None:
            params['device_type'] = device_type
        if type_list:
            # Передаем список типов как multiple values
            for t in type_list:
                # Используем ключ 'type[]'
                params.setdefault('type[]', []).append(t)
        if data is not None:
            params['data'] = data

        # Собираем список пар ключ-значение
        query_parts = []
        for key, value in params.items():
            if isinstance(value, list):
                for v in value:
                    query_parts.append((key, v))
            else:
                query_parts.append((key, value))

        # Кодируем параметры, оставляя '+' как есть
        query_string = urlencode(query_parts, doseq=True, safe='+')

        # Формируем полный URL
        url = f"{base_url}?{query_string}"
        return url

class PredefinedUrls:
    def __init__(self, url_builder, default_url):
        self.builder = url_builder
        self._default_url = default_url

    def default(self, url=None):
        return self.builder.build_event_url(base_url=url or self._default_url)

    def driver_events(self, url=None):
        return self.builder.build_event_url(
            base_url=url or self._default_url,
            driver_uid="driver123",
            date_from="+01.01.2024+",
            date_to="+28.02.2024+",
            type_list=[26, 27],
            data=2
        )

    def device_type_event(self, url=None):
        return self.builder.build_event_url(
            base_url=url or self._default_url,
            device_type="mobile",
            date_from="+01.03.2024+",
            date_to="+31.03.2024+",
            type_list=[38, 4],
            data=3
        )

    def recent_events(self, url=None):
        # За последние сутки
        end = datetime.now()
        start = end - timedelta(days=1)
        return self._build_url_with_dates(start, end, url)

    def today(self, url=None):
        # За сегодня
        today_date = datetime.now().date()
        start = datetime.combine(today_date, datetime.min.time())
        end = datetime.combine(today_date, datetime.max.time())
        return self._build_url_with_dates(start, end, url)

    def yesterday(self, url=None):
        # За вчера
        yesterday_date = (datetime.now() - timedelta(days=1)).date()
        start = datetime.combine(yesterday_date, datetime.min.time())
        end = datetime.combine(yesterday_date, datetime.max.time())
        return self._build_url_with_dates(start, end, url)

    def day_before_yesterday(self, url=None):
        # За позавчера
        day_before = (datetime.now() - timedelta(days=2)).date()
        start = datetime.combine(day_before, datetime.min.time())
        end = datetime.combine(day_before, datetime.max.time())
        return self._build_url_with_dates(start, end, url)

    def current_week(self, url=None):
        # За текущую неделю (понедельник - сегодня)
        today_date = datetime.now().date()
        start_of_week = today_date - timedelta(days=today_date.weekday())
        start = datetime.combine(start_of_week, datetime.min.time())
        end = datetime.combine(today_date, datetime.max.time())
        return self._build_url_with_dates(start, end, url)

    def previous_week(self, url=None):
        # За прошлую неделю
        today_date = datetime.now().date()
        start_of_current_week = today_date - timedelta(days=today_date.weekday())
        start_of_prev_week = start_of_current_week - timedelta(weeks=1)
        end_of_prev_week = start_of_current_week - timedelta(days=1)
        start = datetime.combine(start_of_prev_week, datetime.min.time())
        end = datetime.combine(end_of_prev_week, datetime.max.time())
        return self._build_url_with_dates(start, end, url)

    def current_month(self, url=None):
        # За текущий месяц
        now = datetime.now()
        start = datetime(now.year, now.month, 1)
        end = datetime(now.year, now.month,
                       (start + relativedelta(months=1)) - timedelta(days=1)).replace(
                           hour=23, minute=59, second=59)
        return self._build_url_with_dates(start, end, url)

    def past_month(self, url=None):
        # За прошлый месяц
        now = datetime.now()
        start_of_current_month = datetime(now.year, now.month, 1)
        start_of_prev_month = start_of_current_month - relativedelta(months=1)
        end_of_prev_month = start_of_current_month - timedelta(days=1)
        end_of_prev_month = end_of_prev_month.replace(
            hour=23, minute=59, second=59)
        start = start_of_prev_month
        end = end_of_prev_month
        return self._build_url_with_dates(start, end, url)

    def current_year(self, url=None):
        # За текущий год
        now = datetime.now()
        start = datetime(now.year, 1, 1)
        end = datetime(now.year, 12, 31, 23, 59, 59)
        return self._build_url_with_dates(start, end, url)

    def past_year(self, url=None):
        # За прошлый год
        now = datetime.now()
        start = datetime(now.year - 1, 1, 1)
        end = datetime(now.year - 1, 12, 31, 23, 59, 59)
        return self._build_url_with_dates(start, end, url)

    def _build_url_with_dates(self, start_dt, end_dt, url=None):
        date_from = start_dt.strftime("%d.%m.%Y")
        date_to = end_dt.strftime("%d.%m.%Y")
        date_from_hour = start_dt.strftime("%H")
        date_from_minute = start_dt.strftime("%M")
        date_to_hour = end_dt.strftime("%H")
        date_to_minute = end_dt.strftime("%M")
        return self.builder.build_event_url(
            base_url=url or self._default_url,
            date_from=date_from,
            date_from_hour=date_from_hour,
            date_from_minute=date_from_minute,
            date_to=date_to,
            date_to_hour=date_to_hour,
            date_to_minute=date_to_minute,
            filter_set=1,
            data=1
        )

class UrlProvider(SyncPage, PredefinedUrls):
    def __init__(self, page, default_url=None):
        super().__init__(page)
        self._default_url = default_url
        self.builder = UrlBuilder()
        PredefinedUrls.__init__(self, self.builder, self._default_url)

    def get_driver_events_url(self, url=None):
        return self.driver_events(url)

    def get_device_type_event_url(self, url=None):
        return self.device_type_event(url)

    def get_default_url(self, url=None):
        return self.default(url)

    def get_recent_events_url(self, url=None):
        return self.recent_events(url)

    def get_today_url(self, url=None):
        return self.today(url)

    def get_yesterday_url(self, url=None):
        return self.yesterday(url)

    def get_day_before_yesterday_url(self, url=None):
        return self.day_before_yesterday(url)

    def get_current_week_url(self, url=None):
        return self.current_week(url)

    def get_previous_week_url(self, url=None):
        return self.previous_week(url)

    def get_current_month_url(self, url=None):
        return self.current_month(url)

    def get_past_month_url(self, url=None):
        return self.past_month(url)

    def get_current_year_url(self, url=None):
        return self.current_year(url)

    def get_past_year_url(self, url=None):
        return self.past_year(url)