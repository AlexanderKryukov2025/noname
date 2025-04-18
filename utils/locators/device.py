from selenium.webdriver.common.by import By


class Device:
    CHANGE_TOGGLE_BTN = (By.CSS_SELECTOR, '.justify-content-end button')


class Popup:
    CLOSE_BTN = (By.CSS_SELECTOR, '.modal-dialog button.close')