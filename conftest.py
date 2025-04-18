import pytest
from helpers.webdriver.get_webdriver import WebDriver1600


@pytest.fixture
def driver(request):
    browser = WebDriver1600().get()
    yield browser
    browser.quit()

