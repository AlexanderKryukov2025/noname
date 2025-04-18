import time
import logging


class BrowserLogs:
    def __init__(self, driver, tags=None, entries=1, ts=None, search_type=1, log_type='performance', s=10):
        self.driver = driver
        self.log_type = log_type
        self.seconds = s
        self.search_type = search_type
        self.entry_num = entries
        self.tags = tags
        self.global_storage = []
        self.target_storage = []
        self.get_timestamp(ts)
        self.get_log()

    def get_timestamp(self, ts):
        if isinstance(ts, bool) and ts:
            self.timestamp = round(time.time() * 1000)
        else:
            self.timestamp = ts

    def get_log(self):
        timing = time.time()
        while time.time() - timing < self.seconds:
            self.logs = self.driver.get_log(self.log_type)

            if len(self.logs):
                if self.take_all_logs():
                    continue  # если не используем ключевые слова, то не используем фильтр и собираем все логи

                for entry in self.logs:
                    # Получение записей логов, с определенного момента времени
                    if self.skip_outdated_logs(entry):
                        continue

                    self.global_storage.append(entry)
                    self.matches = []

                    if self.search_type == 1:
                        self._standard_search(entry)
                    elif self.search_type == 2:
                        self._alternative_search(entry)
                    elif self.search_type == 3:
                        self._sequential_search(entry)

        else:
            logging.warning(f'{self.__class__.__name__}: search time is over')

    def take_all_logs(self):
        if not self.tags:
            for entry in self.logs:  # Если нужны все логи с момента запуска
                self.global_storage.append(entry)
            return True

    def skip_outdated_logs(self, entry):
        if self.timestamp:
            return entry if self.timestamp < entry['timestamp'] else None

    def save_result(self, entry, tags):
        # Если число совпадений в одной строке равно количеству тегов,
        # то искомый результат записываем в отдельное хранилище
        if len(self.matches) == len(tags):
            self.target_storage.append(entry)

            # Если достигли желаемого числа записей в логах с таким совпадением
            if len(self.target_storage) == self.entry_num:
                return True

    def _standard_search(self, entry):
        [self.matches.append(t) for t in self.tags if t in str(entry)]
        if self.save_result(entry, self.tags):
            return

    def _alternative_search(self, entry):
        [self.matches.append(t) for tag in self.tags for t in tag if t in str(entry)]
        if self.save_result(entry, self.tags):
            return

    def _sequential_search(self, entry):
        for idx, tag in enumerate(self.tags):
            if isinstance(tag, list):
                if self.matches:
                    self.matches = []
                [self.matches.append(t) for t in tag if t in str(entry)]
                if len(self.matches) == len(tag):
                    self.target_storage.append(entry)
                    self.tags.pop(idx)
                    break
            else:
                if tag in str(entry):
                    self.target_storage.append(entry)
                    self.tags.pop(idx)
                    break
        else:  # Выходим, если перебрали все теги
            return

# import time
# import logging
#
#
# class BrowserLogs:
#     def __init__(self, driver, tags=None, entries=1, ts=None, search_type=1, log_type='performance', s=10):
#         self.driver = driver
#         self.log_type = log_type
#         self.seconds = s
#         self.search_type = search_type
#         self.entry_num = entries
#         self.tags = tags
#         self.global_storage = []
#         self.target_storage = []
#         self.get_timestamp(ts)
#         self.get_log()
#
#     def get_timestamp(self, ts):
#         if isinstance(ts, bool) and ts:
#             self.timestamp = round(time.time() * 1000)
#         else:
#             self.timestamp = ts
#
#     def take_all_logs(self):
#         if not self.tags:
#             for entry in self.logs:  # если нужны все логи с момента запуска
#                 self.global_storage.append(entry)
#             return True
#
#     def skip_outdated_logs(self, entry):
#         if self.timestamp:
#             if not self.timestamp < entry['timestamp']:
#                 return entry
#
#     def save_result(self, entry, tags):
#         # если число совпадений в одной строге равно количеству тегов,
#         # то искомый результат записываем в отдельное хранилище
#         if len(self.matches) == len(tags):
#
#             self.target_storage.append(entry)
#             # и далее сверяемся с числом желаемых записей в логах с таким совпадением
#             if len(self.target_storage) == self.entry_num:
#                 return True
#
#     def get_log(self):
#         timing = time.time()
#         while time.time() - timing < self.seconds:
#             self.logs = self.driver.get_log(self.log_type)
#             if len(self.logs):
#
#                 if self.take_all_logs():
#                     continue  # если не используем ключевые слова, то не используем фильтр и собираем все логи
#
#                 for entry in self.logs:
#                     # получения записей логов, с определенного момента времени
#                     if self.skip_outdated_logs(entry):
#                         continue
#
#                     self.global_storage.append(entry)
#
#                     self.matches = []
#                     if self.search_type == 1:
#                         # стандартный поиск совпадений всех тегов в каждой записи с логами, пример тегов:
#                         # ['Network.loadingFinished']
#                         [self.matches.append(t) for t in self.tags if t in str(entry)]
#                         if self.save_result(entry, self.tags):
#                             return
#
#                     elif self.search_type == 2:
#                         # для альтернативных вариантов поиска, пример:
#                         #   видео или аудио (в одной строке),
#                         # чтобы использовать этот тип, в качестве входных данных нужно отправить список тегов, пример:
#                         #   [['icon-flag-en', 'icon-flag-ru']]
#
#                         [self.matches.append(t) for tag in self.tags for t in tag if t in str(entry)]
#                         if self.save_result(entry, self.tags):
#                             return
#
#                     elif self.search_type == 3:
#                         # для случаев когда нужно найти последовательность записей, пример:
#                         # [
#                         #     ['Network.responseReceived', 'icon-toggle-name-off.svg'],
#                         #     'Network.dataReceived',
#                         #     'Network.loadingFinished'
#                         # ]
#                         # попытка найти следующие 2х тега будет предпринята только в случае успеха поиска 1го тега
#                         for idx, tag in enumerate(self.tags):
#                             if isinstance(tag, list):
#                                 if self.matches:
#                                     self.matches = []
#                                 [self.matches.append(t) for t in tag if t in str(entry)]
#                                 if len(self.matches) == len(tag):
#                                     self.target_storage.append(entry)
#                                     self.tags.pop(idx)
#                                     break
#                                 else:
#                                     break
#                             else:
#                                 if tag in str(entry):
#                                     self.target_storage.append(entry)
#                                     self.tags.pop(idx)
#                                     break
#                                 else:
#                                     break
#                         else:  # выходим если перебрали все теги
#                             return
#
#         else:
#             logging.warning(f'{self.__class__.__name__}: search time is over')
