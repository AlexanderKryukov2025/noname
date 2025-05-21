import gspread

filename = 'statistics_experiments_full'


class SortCategoryAirat:
    def __init__(self):

        self.gc = gspread.service_account(filename="./creds/stats-460013-559d22110e26.json")
        self.wks = self.gc.open(filename)
        self.sheets_count = len(self.wks.worksheets())
        self.data_pages = self.odd_pages = [i - 1 for i in range(1, self.sheets_count + 1) if i % 2 == 1][:-1]

        self.events_dict3 = {
            "Засыпание": 0,
            "Телефон": 0,
            "Курение": 0,
            "Взгляд в сторону": 0,
            "Ремень": 0,
            "Еда": 0,
            "Водитля нет в кадре": 0,
            "Заслон камеры": 0,
        }

        self.events_dict4 = {
            "Засыпание": 0,
            "Телефон": 0,
            "Курение": 0,
            "Взгляд в сторону": 0,
            "Ремень": 0,
            "Еда": 0,
            "Водитля нет в кадре": 0,
            "Заслон камеры": 0,
        }

        self.diffs1 = []
        self.diffs2 = []
        self.device1 = None
        self.device2 = None

    def calculate_diffs_row(self, sheet, row_num):
        row_values = sheet.row_values(row_num)
        device_name = row_values.pop(0)
        diffs = [
            int(row_values[i]) - int(row_values[i + 1])
            for i in range(0, len(row_values), 2)
        ]
        return diffs, device_name

    def get_diffs(self, sheet_num=0, row_num=3):
        sheet = self.wks.get_worksheet(sheet_num)
        self.diffs1, self.device1 = self.calculate_diffs_row(sheet, row_num)
        self.diffs2, self.device2 = self.calculate_diffs_row(sheet, row_num + 1)

    def set_values_dict(self, diffs, events_dict):
        for i, v in enumerate(events_dict):
            events_dict[v] = diffs[i]

    def update_dicts(self):
        self.set_values_dict(self.diffs1, self.events_dict3)
        self.set_values_dict(self.diffs2, self.events_dict4)

    def sort_update_dictionary(self, sheet_num=1, dictionary_index=1, device_name='', start_row=11):
        sheet = self.wks.get_worksheet(sheet_num)
        if dictionary_index == 0:
            events_dict = self.events_dict3
            start_row = start_row
            category_col = 'I'
            value_col = 'J'
        else:
            events_dict = self.events_dict4
            start_row = start_row
            category_col = 'L'
            value_col = 'M'

        # сортируем по убыванию
        # sorted_items = sorted(events_dict.items(), key=lambda x: x[1], reverse=True)
        sorted_items = sorted(events_dict.items(), key=lambda x: x[0])  # по имени события
        sorted_items.insert(0, (device_name, ''))

        # подготовим список запросов для batch_update
        requests = []
        row_idx = start_row
        for category, diff in sorted_items:
            requests.append({
                'range': f'{category_col}{row_idx}',
                'values': [[category]]
            })
            requests.append({
                'range': f'{value_col}{row_idx}',
                'values': [[diff]]
            })
            row_idx += 1

        sheet.batch_update(requests)

    def sort_update_category_values(self, sheet_num=1, update_count=0, start_row=0):
        if update_count == 0:
            self.sort_update_dictionary(sheet_num, 0)
        elif update_count == 1:
            self.sort_update_dictionary(sheet_num, 1)
        elif update_count == 2:
            self.sort_update_dictionary(sheet_num, 0, self.device1, start_row)
            self.sort_update_dictionary(sheet_num, 1, self.device2, start_row)


class CollectRatio:
    def __init__(self):
        self.gc = gspread.service_account(filename='./creds/stats-460013-559d22110e26.json')
        self.wks = self.gc.open(filename)
        self.all_sheets = self.wks.worksheets()

        self.airat_2_5 = {}
        self.airat_3_5 = {}
        self.startrans_2_5 = {}
        self.startrans_3_5 = {}

    def collect_dates_ratios(self, cells_address):
        for i in range(1, len(self.all_sheets)):
            if i % 2 != 0:
                sheet = self.all_sheets[i]
                stats_date = sheet.acell('B32').value
                airat_2_5 = sheet.acell(cells_address[0]).value
                airat_3_5 = sheet.acell(cells_address[1]).value
                startrans_2_5 = sheet.acell(cells_address[2]).value
                startrans_3_5 = sheet.acell(cells_address[3]).value

                self.airat_2_5[stats_date] = airat_2_5
                self.airat_3_5[stats_date] = airat_3_5
                self.startrans_2_5[stats_date] = startrans_2_5
                self.startrans_3_5[stats_date] = startrans_3_5

    def update_date_ratio(self, groups, data_dict):
        sheet = self.all_sheets[-1]
        requests = []
        for group in groups:
            for index, (date, value) in enumerate(data_dict.items(), start=3):
                requests.append({'range': f'{group[0]}{index}', 'values': [[date]]})
                requests.append({'range': f'{group[1]}{index}', 'values': [[value]]})

        sheet.batch_update([{'range': r['range'], 'values': r['values']} for r in requests])
        data_dict.clear()


# inst = SortCategoryAirat()
# inst.get_diffs(0, 3)
# inst.update_dicts()
# inst.sort_update_category_values(0, 2, 11)

inst = SortCategoryAirat()
for data_page in inst.data_pages:
    # забирает показатели двух соседних устройств "Айрат" на 1й странице data и выводит разницу
    inst.get_diffs(data_page, 3)
    inst.update_dicts()
    inst.sort_update_category_values(data_page, 2, 11)

    # забирает показатели двух соседних устройств "Стартранс" на 1й странице data и выводит разницу
    inst.get_diffs(data_page, 7)
    inst.update_dicts()
    inst.sort_update_category_values(data_page, 2, 21)

# забирает данные со страницы stats из группы "Коэффициент засыпания"
# и копирует в diagrams, в группу "Коэффициент"
a = CollectRatio()
a.collect_dates_ratios(['B23', 'B24', 'B26', 'B27'])
a.update_date_ratio([['A', 'B']], a.airat_2_5)
a.update_date_ratio([['C', 'D']], a.airat_3_5)
a.update_date_ratio([['E', 'F']], a.startrans_2_5)
a.update_date_ratio([['G', 'H']], a.startrans_3_5)

# забирает данные со страницы stats из группы "Среднее значение собранных (всего) событий"
# и копирует в diagrams, в группу "Общее количество собранныз событий"
a.collect_dates_ratios(['B3', 'B4', 'B6', 'B7'])
a.update_date_ratio([['I', 'J']], a.airat_2_5)
a.update_date_ratio([['K', 'L']], a.airat_3_5)
a.update_date_ratio([['M', 'N']], a.startrans_2_5)
a.update_date_ratio([['O', 'P']], a.startrans_3_5)
