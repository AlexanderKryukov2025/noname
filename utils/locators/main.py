
from selenium.webdriver.common.by import By


class Main:
    MENU_LIST = (By.CSS_SELECTOR, 'ul.navbar-nav:not(.navbar-right) li')
    DEVICES_BTN_RU = (By.LINK_TEXT, 'Устройства')
    DEVICES_BTN_ENG = (By.LINK_TEXT, 'Devices')