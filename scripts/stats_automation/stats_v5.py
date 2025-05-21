import gspread

FILENAME = 'statistics_experiments_short'
CREDENTIALS_PATH = "./creds/stats-460013-559d22110e26.json"

class SortCategoryAirat:
    def __init__(self):
        self.gc = gspread.service_account(filename=CREDENTIALS_PATH)
        self.wks = self.gc.open(FILENAME)
        self.data_pages = [i - 1 for i in range(1, len(self.wks.worksheets()) + 1) if i % 2 == 1][:-1]

        self.events_dict_template = {
            "Засыпание": 0,
            "Телефон": 0,
            "Курение": 0,
            "Взгляд в сторону": 0,
            "Ремень": 0,
            "Еда": 0,
            "Водитля нет в кадре": 0,
            "Заслон камеры": 0,
        }
        self.events_dict3 = self.events_dict4 = self.events_dict_template.copy()

        self.diffs1 = self.diffs2 = []
        self.device1 = self.device2 = None

    def _calculate_diffs_row(self, sheet, row_num):
        row = sheet.row_values(row_num)
        device_name = row.pop(0)
        diffs = [int(row[i]) - int(row[i + 1]) for i in range(0, len(row), 2)]
        return diffs, device_name

    def get_diffs(self, sheet_idx=0, row_num=3):
        sheet = self.wks.get_worksheet(sheet_idx)
        self.diffs1, self.device1 = self._calculate_diffs_row(sheet, row_num)
        self.diffs2, self.device2 = self._calculate_diffs_row(sheet, row_num + 1)

    def _set_dict_values(self, diffs, events_dict):
        for key, value in zip(events_dict.keys(), diffs):
            events_dict[key] = value

    def update_dicts(self):
        self._set_dict_values(self.diffs1, self.events_dict3)
        self._set_dict_values(self.diffs2, self.events_dict4)

    def sort_update_dictionary(self, sheet_idx=1, dict_idx=1, device_name='', start_row=11):
        sheet = self.wks.get_worksheet(sheet_idx)
        events_dict = self.events_dict3 if dict_idx == 0 else self.events_dict4
        category_col, value_col = ('I', 'J') if dict_idx == 0 else ('L', 'M')
        sorted_items = sorted(events_dict.items(), key=lambda x: x[0])
        sorted_items.insert(0, (device_name, ''))

        requests = []
        row = start_row
        for category, diff in sorted_items:
            requests.extend([
                {'range': f'{category_col}{row}', 'values': [[category]]},
                {'range': f'{value_col}{row}', 'values': [[diff]]}
            ])
            row += 1
        sheet.batch_update(requests)

    def sort_update_category_values(self, sheet_idx=1, update_count=0, start_row=0):
        if update_count == 0:
            self.sort_update_dictionary(sheet_idx, 0, start_row=start_row)
        elif update_count == 1:
            self.sort_update_dictionary(sheet_idx, 1, start_row=start_row)
        elif update_count == 2:
            self.sort_update_dictionary(sheet_idx, 0, device_name=self.device1, start_row=start_row)
            self.sort_update_dictionary(sheet_idx, 1, device_name=self.device2, start_row=start_row)

class CollectRatio:
    def __init__(self):
        self.gc = gspread.service_account(filename=CREDENTIALS_PATH)
        self.wks = self.gc.open(FILENAME)
        self.sheets = self.wks.worksheets()

        # Инициализация словарей
        self.airat_2_5 = {}
        self.airat_3_5 = {}
        self.startrans_2_5 = {}
        self.startrans_3_5 = {}

    def collect_dates_ratios(self, cells_addresses):
        for sheet in self.sheets[1::2]:  # перебираем нечетные страницы
            date = sheet.acell('B32').value
            vals = [sheet.acell(addr).value for addr in cells_addresses]
            self.airat_2_5[date], self.airat_3_5[date], self.startrans_2_5[date], self.startrans_3_5[date] = vals

    def _update_date_ratio(self, groups, data_dict):
        sheet = self.sheets[-1]
        requests = []
        for group in groups:
            for idx, (date, value) in enumerate(data_dict.items(), start=3):
                requests.append({'range': f'{group[0]}{idx}', 'values': [[date]]})
                requests.append({'range': f'{group[1]}{idx}', 'values': [[value]]})
        sheet.batch_update(requests)
        data_dict.clear()

    def update_date_ratio(self, groups, data_dict):
        self._update_date_ratio(groups, data_dict)

inst = SortCategoryAirat()
for page in inst.data_pages:
    # Разницы для "Айрат"
    inst.get_diffs(page, 3)
    inst.update_dicts()
    inst.sort_update_category_values(page, 2, 11)

    # Разницы для "Стартранс"
    inst.get_diffs(page, 7)
    inst.update_dicts()
    inst.sort_update_category_values(page, 2, 21)

# Обновление коэффициентов и событий
a = CollectRatio()

# Коэффициенты засыпания
a.collect_dates_ratios(['B23','B24','B26','B27'])
a.update_date_ratio([['A','B']], a.airat_2_5)
a.update_date_ratio([['C','D']], a.airat_3_5)
a.update_date_ratio([['E','F']], a.startrans_2_5)
a.update_date_ratio([['G','H']], a.startrans_3_5)

# Среднее количество событий
a.collect_dates_ratios(['B3','B4','B6','B7'])
a.update_date_ratio([['I','J']], a.airat_2_5)
a.update_date_ratio([['K','L']], a.airat_3_5)
a.update_date_ratio([['M','N']], a.startrans_2_5)
a.update_date_ratio([['O','P']], a.startrans_3_5)