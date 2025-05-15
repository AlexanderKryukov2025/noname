import pytest

from rest.cluster import Cluster

def pytest_addoption(parser):
    parser.addoption('--driver', action='store', default='chromium', help='Browser: chromium, firefox, webkit')
    parser.addoption('--headless', action='store_true', help='Browser headless-mode')


@pytest.fixture(scope='class')
def cluster():
    cluster = Cluster()
    return cluster
