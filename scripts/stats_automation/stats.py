import gspread
import itertools
import time


class SortCategoryAirat:
    def __init__(self):
        self.gc = gspread.service_account(filename="./creds/stats-460013-559d22110e26.json")
        self.wks = self.gc.open("statistics_experiments")

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

    def calculate_diffs_row(self, sheet_num, row_num):
        diffs = []
        row_values = self.wks.get_worksheet(sheet_num).row_values(row_num)
        row_values.pop(0)

        for value_index in range(0, len(row_values), 2):
            value_diff = int(row_values[value_index]) - int(row_values[value_index + 1])
            diffs.append(value_diff)

        return diffs

    def get_diffs(self, sheet_num=0, row_num=3, rows_count=2):
        match rows_count:
            case 0:
                self.diffs3 = self.calculate_diffs_row(sheet_num, row_num)

            case 1:
                self.diffs4 = self.calculate_diffs_row(sheet_num, row_num + 1)

            case 2:
                self.diffs3 = self.calculate_diffs_row(sheet_num, row_num)
                self.diffs4 = self.calculate_diffs_row(sheet_num, row_num + 1)

    def set_values_dict3(self):
        for i, v in enumerate(self.events_dict3):
            self.events_dict3[v] = self.diffs3[i]

    def set_values_dict4(self):
        for i, v in enumerate(self.events_dict4):
            self.events_dict4[v] = self.diffs4[i]

    def update_dict_value(self, all_dictionary=2):
        match all_dictionary:
            case 0:
                self.set_values_dict3()
            case 1:
                self.set_values_dict4()
            case 2:
                self.set_values_dict3()
                self.set_values_dict4()

    def sort_update_dictionary(self, sheet_num=1,  dictionary=1):
        match dictionary:
            case 0:
                starting_cell = 11
                descending_categories_by_diff = sorted(self.events_dict3.items(), key=lambda x: x[1], reverse=True)

                for data in descending_categories_by_diff:
                    category, diff = data

                    self.wks.get_worksheet(sheet_num).update([[category]], ('I' + f'{starting_cell}'))
                    self.wks.get_worksheet(sheet_num).update([[diff]], ('I' + f'{starting_cell + 1}'))

                    starting_cell += 3

            case 1:
                starting_cell = 11
                descending_categories_by_diff = sorted(self.events_dict4.items(), key=lambda x: x[1], reverse=True)

                for data in descending_categories_by_diff:
                    category, diff = data

                    self.wks.get_worksheet(sheet_num).update([[category]], ('L' + f'{starting_cell}'))
                    self.wks.get_worksheet(sheet_num).update([[diff]], ('L' + f'{starting_cell + 1}'))

                    starting_cell += 3

    def sort_update_category_values(self, sheet_num=1, update_count=0):

        match update_count:
            case 0:
                self.sort_update_dictionary(sheet_num,0)
            case 1:
                self.sort_update_dictionary(sheet_num,1)
            case 2:
                self.sort_update_dictionary(sheet_num,0)
                self.sort_update_dictionary(sheet_num,1)


class CollectRatio:
    def __init__(self):
        self.gc = gspread.service_account(filename='./creds/stats-460013-559d22110e26.json')
        self.wks = self.gc.open("statistics_experiments")
        self.weekly_stats = self.wks.worksheet('diagrams')
        self.all_sheets = self.wks.worksheets()

        self.airat_2_5 = {}
        self.airat_3_5 = {}

        self.startrans_2_5 = {}
        self.startrans_3_5 = {}

    def handle_quota_on_update(self):
        pass

    def collect_dates_ratios(self, cells_address):

        date_cell_location = 'B32'

        for i in range(1, len(self.all_sheets)):
            if i % 2 != 0:
                stats_date = self.wks.get_worksheet(i).acell(date_cell_location)

                airat_2_5 = self.wks.get_worksheet(i).acell(cells_address[0])
                airat_3_5 = self.wks.get_worksheet(i).acell(cells_address[1])

                startrans_2_5 = self.wks.get_worksheet(i).acell(cells_address[2])
                startrans_3_5 = self.wks.get_worksheet(i).acell(cells_address[3])

                self.airat_2_5.update({stats_date.value: airat_2_5.value})
                self.airat_3_5.update({stats_date.value: airat_3_5.value})

                self.startrans_2_5.update({stats_date.value: startrans_2_5.value})
                self.startrans_3_5.update({stats_date.value: startrans_3_5.value})


    def update_date_ratio(self, cells, dictionary):

        diagrams_sheet = self.all_sheets[-1]

        for group in cells:
            for index, (date, value) in enumerate(dictionary.items(), 3):

                try:
                    diagrams_sheet.update([[date]], f'{group[0]}{index}')
                    diagrams_sheet.update([[value]], f'{group[1]}{index}')
                    pass

                except gspread.exceptions.APIError:
                    time.sleep(60)
                    diagrams_sheet.update([[date]], f'{group[0]}{index}')
                    diagrams_sheet.update([[value]], f'{group[1]}{index}')
                    continue

        dictionary.clear()


inst = SortCategoryAirat()
inst.get_diffs(0, 3, 2)
inst.update_dict_value()
inst.sort_update_category_values(0, 2)


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

