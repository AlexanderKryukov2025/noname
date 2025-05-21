import gspread

FILENAME = 'statistics_experiments_short'
CREDENTIALS_PATH = "./creds/stats-460013-559d22110e26.json"

# Константы для диапазонов ячеек и настроек
CATEGORIES_EVENTS = {
    "Засыпание": 0,
    "Телефон": 0,
    "Курение": 0,
    "Взгляд в сторону": 0,
    "Ремень": 0,
    "Еда": 0,
    "Водитля нет в кадре": 0,
    "Заслон камеры": 0,
}

# Колонки для обновления данных в листах
CATEGORY_COLUMNS = {0: ('I', 'J'), 1: ('L', 'M')}  # Для dict_idx 0 и 1

class GoogleSheetHelper:
    """Общий помощник для работы с Google Sheets."""
    def __init__(self, filename, credentials_path):
        self.gc = gspread.service_account(filename=credentials_path)
        self.wks = self.gc.open(filename)
        self.sheets = self.wks.worksheets()

    def get_worksheet(self, index):
        """Получить лист по индексу."""
        return self.sheets[index]

    def batch_update(self, sheet, requests):
        """Выполнить пакетное обновление."""
        sheet.batch_update(requests)

    def get_cell_value(self, sheet, cell_address):
        """Получить значение ячейки."""
        return sheet.acell(cell_address).value

class SortCategoryAirat:
    def __init__(self, sheet_helper):
        self.sheet_helper = sheet_helper
        self.data_pages = [i - 1 for i in range(1, len(self.sheet_helper.sheets) + 1) if i % 2 == 1][:-1]
        self.events_template = CATEGORIES_EVENTS.copy()

        # Изначальные словари для diffs
        self.events_dicts = [
            self.events_template.copy(),
            self.events_template.copy()
        ]
        self.diffs = [[], []]
        self.devices = [None, None]

    def _calculate_diffs_row(self, sheet, row_num):
        row = sheet.row_values(row_num)
        device_name = row.pop(0)
        diffs = [int(row[i]) or 0 - int(row[i + 1]) or 0 for i in range(0, len(row), 2)]
        return diffs, device_name

    def get_diffs(self, sheet_idx=0, row_num=3):
        sheet = self.sheet_helper.get_worksheet(sheet_idx)
        self.diffs[0], self.devices[0] = self._calculate_diffs_row(sheet, row_num)
        self.diffs[1], self.devices[1] = self._calculate_diffs_row(sheet, row_num + 1)

    def _update_events_dicts(self):
        for i in range(2):
            for key, value in zip(self.events_template.keys(), self.diffs[i]):
                self.events_dicts[i][key] = value

    def update_all_dicts(self):
        self._update_events_dicts()

    def _sort_and_update_sheet(self, sheet_idx, dict_idx, device_name='', start_row=11):
        sheet = self.sheet_helper.get_worksheet(sheet_idx)
        events_dict = self.events_dicts[dict_idx]
        category_col, value_col = CATEGORY_COLUMNS[dict_idx]
        sorted_items = sorted(events_dict.items(), key=lambda x: x[0])
        sorted_items.insert(0, (device_name, ''))

        requests = []
        row = start_row
        for category, diff in sorted_items:
            requests.append({'range': f'{category_col}{row}', 'values': [[category]]})
            requests.append({'range': f'{value_col}{row}', 'values': [[diff]]})
            row += 1

        self.sheet_helper.batch_update(sheet, requests)

    def sort_update_category_values(self, sheet_idx=1, update_count=0, start_row=0):
        if update_count == 0:
            self._sort_and_update_sheet(sheet_idx, 0, start_row=start_row)
        elif update_count == 1:
            self._sort_and_update_sheet(sheet_idx, 1, start_row=start_row)
        elif update_count == 2:
            self._sort_and_update_sheet(sheet_idx, 0, device_name=self.devices[0], start_row=start_row)
            self._sort_and_update_sheet(sheet_idx, 1, device_name=self.devices[1], start_row=start_row)

class CollectRatio:
    def __init__(self, sheet_helper):
        self.sheet_helper = sheet_helper
        self.airat_2_5 = {}
        self.airat_3_5 = {}
        self.startrans_2_5 = {}
        self.startrans_3_5 = {}

    def collect_dates_ratios(self, cells_addresses):
        """Сбор данных из указанных ячеек по нечетным листам."""
        for sheet in self.sheet_helper.sheets[1::2]:
            date = self.sheet_helper.get_cell_value(sheet, 'B32')
            vals = [self.sheet_helper.get_cell_value(sheet, addr) for addr in cells_addresses]
            # Распределяем значения по словарям
            self.airat_2_5[date], self.airat_3_5[date], self.startrans_2_5[date], self.startrans_3_5[date] = vals

    def _update_date_ratio(self, groups, data_dict):
        """Обновление данных по датам на последнем листе."""
        sheet = self.sheet_helper.sheets[-1]
        requests = []
        for group in groups:
            for idx, (date, value) in enumerate(data_dict.items(), start=3):
                requests.append({'range': f'{group[0]}{idx}', 'values': [[date]]})
                requests.append({'range': f'{group[1]}{idx}', 'values': [[value]]})
        self.sheet_helper.batch_update(sheet, requests)
        data_dict.clear()

    def update_date_ratio(self, groups, data_dict):
        self._update_date_ratio(groups, data_dict)

# Инициализация хелпера
sheet_helper = GoogleSheetHelper(FILENAME, CREDENTIALS_PATH)
# Обработка категорий
category_processor = SortCategoryAirat(sheet_helper)

for page in category_processor.data_pages:
    # Разницы для "Айрат":
    # забирает показатели двух соседних устройств "Айрат" на 1й странице data и выводит разницу
    category_processor.get_diffs(page, 3)
    category_processor.update_all_dicts()
    category_processor.sort_update_category_values(page, 2, 11)

    # Разницы для "Стартранс":
    # забирает показатели двух соседних устройств "Стартранс" на 1й странице data и выводит разницу
    category_processor.get_diffs(page, 7)
    category_processor.update_all_dicts()
    category_processor.sort_update_category_values(page, 2, 21)

# Обновление коэффициентов и событий
collector = CollectRatio(sheet_helper)

# Коэффициенты засыпания:
# забирает данные со страницы stats из группы "Коэффициент засыпания"
# и копирует в diagrams, в группу "Коэффициент"
collector.collect_dates_ratios(['B23','B24','B26','B27'])
collector.update_date_ratio([['A','B']], collector.airat_2_5)
collector.update_date_ratio([['C','D']], collector.airat_3_5)
collector.update_date_ratio([['E','F']], collector.startrans_2_5)
collector.update_date_ratio([['G','H']], collector.startrans_3_5)

# Среднее количество событий:
# забирает данные со страницы stats из группы "Среднее значение собранных (всего) событий"
# и копирует в diagrams, в группу "Общее количество собранныз событий"
collector.collect_dates_ratios(['B3','B4','B6','B7'])
collector.update_date_ratio([['I','J']], collector.airat_2_5)
collector.update_date_ratio([['K','L']], collector.airat_3_5)
collector.update_date_ratio([['M','N']], collector.startrans_2_5)
collector.update_date_ratio([['O','P']], collector.startrans_3_5)