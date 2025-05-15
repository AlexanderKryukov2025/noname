import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Locators:
    def __call__(self, page_name):
        return self.__get_a_locator(page_name)

    @staticmethod
    def __get_a_locator(page_name):
        with open(
                f"{BASE_DIR}/locators/{page_name}.json", "r", encoding="utf8"
        ) as file:
            locators_info = json.load(file)
        return locators_info
