import pytest

from helpers.webdriver.get_webdriver import WebDriver1600
from rest.cluster import Cluster


@pytest.fixture
def driver(request):
    browser = WebDriver1600().get()
    yield browser
    browser.quit()


@pytest.fixture(scope='class')
def cluster():
    cluster = Cluster()
    return cluster
