from selenium.webdriver.common.by import By


class Login:
    EMAIL_INPUT = (By.CSS_SELECTOR, '#email')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '#password')
    SUBMIT_BTN = (By.CSS_SELECTOR, '[type="submit"].btn')
