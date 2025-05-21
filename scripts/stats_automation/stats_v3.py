import openpyxl
import itertools
import time

class SortCategoryAirat:
    def __init__(self, filename="./statistics_experiments2.xlsx"):
        # Открываем локальный файл Excel
        self.wb = openpyxl.load_workbook(filename)
        # Предположим, что работа идет со всеми листами
        # Для получения листа по имени или индексу
        self.worksheets = self.wb.worksheets

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

        self.diffs3 = []
        self.diffs4 = []

    def get_sheet(self, sheet_index):
        return self.worksheets[sheet_index]

    def calculate_diffs_row(self, sheet_index, row_num):
        sheet = self.get_sheet(sheet_index)
        row_values = [cell.value for cell in sheet[row_num]]

        # Удаляем первый элемент (префикс)
        row_values = row_values[1:]
        diffs = []

        for i in range(0, len(row_values), 2):
            # Предполагается, что значения есть и они цифры
            val1 = int(row_values[i]) if row_values[i] is not None else 0
            val2 = int(row_values[i+1]) if row_values[i+1] is not None else 0
            diffs.append(val1 - val2)

        return diffs

    def get_diffs(self, sheet_num=0, row_num=3, rows_count=2):
        if rows_count == 0:
            self.diffs3 = self.calculate_diffs_row(sheet_num, row_num)
        elif rows_count == 1:
            self.diffs4 = self.calculate_diffs_row(sheet_num, row_num + 1)
        elif rows_count == 2:
            self.diffs3 = self.calculate_diffs_row(sheet_num, row_num)
            self.diffs4 = self.calculate_diffs_row(sheet_num, row_num + 1)

    def set_values_dict3(self):
        for i, v in enumerate(self.events_dict3):
            self.events_dict3[v] = self.diffs3[i]

    def set_values_dict4(self):
        for i, v in enumerate(self.events_dict4):
            self.events_dict4[v] = self.diffs4[i]

    def update_dict_value(self, all_dictionary=2):
        if all_dictionary == 0:
            self.set_values_dict3()
        elif all_dictionary == 1:
            self.set_values_dict4()
        elif all_dictionary == 2:
            self.set_values_dict3()
            self.set_values_dict4()

    def sort_update_dictionary(self, sheet_num=1, dictionary=1):
        sheet = self.get_sheet(sheet_num)
        if dictionary == 0:
            starting_cell = 10
            descending = sorted(self.events_dict3.items(), key=lambda x: x[1], reverse=True)
            col_letter_category = 'I'
            col_letter_diff = 'J'
        elif dictionary == 1:
            starting_cell = 10
            descending = sorted(self.events_dict4.items(), key=lambda x: x[1], reverse=True)
            col_letter_category = 'L'
            col_letter_diff = 'M'
        else:
            return

        for data in descending:
            category, diff = data
            row_idx = starting_cell
            # Обновляем ячейки
            sheet[f'{col_letter_category}{row_idx}'].value = category
            sheet[f'{col_letter_diff}{row_idx}'].value = diff
            starting_cell += 3

    def sort_update_category_values(self, sheet_num=1, update_count=0):
        if update_count == 0:
            self.sort_update_dictionary(sheet_num, 0)
        elif update_count == 1:
            self.sort_update_dictionary(sheet_num, 1)
        elif update_count == 2:
            self.sort_update_dictionary(sheet_num, 0)
            self.sort_update_dictionary(sheet_num, 1)

    def save(self, filename="./statistics_experiments2.xlsx"):
        self.wb.save(filename)


class CollectRatio:
    def __init__(self, filename="./statistics_experiments2.xlsx"):
        self.wb = openpyxl.load_workbook(filename)
        # Предположим, что есть лист с именем 'diagrams'
        self.diagrams_sheet = self.wb['diagrams']
        self.all_sheets = self.wb.worksheets

        self.airat_2_5 = {}
        self.airat_3_5 = {}
        self.startrans_2_5 = {}
        self.startrans_3_5 = {}

    def handle_quota_on_update(self):
        pass

    def collect_dates_ratios(self, cells_address):
        date_cell_location = 'B32'

        for i, sheet in enumerate(self.all_sheets):
            if i % 2 != 0:
                stats_date_cell = sheet[date_cell_location]
                date_value = stats_date_cell.value

                airat_2_5_cell = sheet[cells_address[0]]
                airat_3_5_cell = sheet[cells_address[1]]
                startrans_2_5_cell = sheet[cells_address[2]]
                startrans_3_5_cell = sheet[cells_address[3]]

                self.airat_2_5[date_value] = airat_2_5_cell.value
                self.airat_3_5[date_value] = airat_3_5_cell.value
                self.startrans_2_5[date_value] = startrans_2_5_cell.value
                self.startrans_3_5[date_value] = startrans_3_5_cell.value

    def update_date_ratio(self, cells, dictionary):
        # cells - список из групп ячеек, например [['A', 'B']]
        # dictionary - словарь с данными
        for group in cells:
            for index, (date, value) in enumerate(dictionary.items(), start=3):
                try:
                    self.diagrams_sheet[f'{group[0]}{index}'].value = date
                    self.diagrams_sheet[f'{group[1]}{index}'].value = value
                except Exception:
                    time.sleep(60)
                    self.diagrams_sheet[f'{group[0]}{index}'].value = date
                    self.diagrams_sheet[f'{group[1]}{index}'].value = value
        dictionary.clear()

    def save(self, filename="./statistics_experiments2.xlsx"):
        self.wb.save(filename)


# Использование:
inst = SortCategoryAirat()
inst.get_diffs(0, 3, 2)
inst.update_dict_value()
inst.sort_update_category_values(0, 2)
inst.save()

a = CollectRatio()
a.collect_dates_ratios(['B23', 'B24', 'B26', 'B27'])
a.update_date_ratio([['A', 'B']], a.airat_2_5)
a.update_date_ratio([['C', 'D']], a.airat_3_5)
a.update_date_ratio([['E', 'F']], a.startrans_2_5)
a.update_date_ratio([['G', 'H']], a.startrans_3_5)

a.collect_dates_ratios(['B3', 'B4', 'B6', 'B7'])
a.update_date_ratio([['I', 'J']], a.airat_2_5)
a.update_date_ratio([['K', 'L']], a.airat_3_5)
a.update_date_ratio([['M', 'N']], a.startrans_2_5)
a.update_date_ratio([['O', 'P']], a.startrans_3_5)

# Не забудьте сохранить изменения в файле
inst.save()
a.save()