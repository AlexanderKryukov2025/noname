import allure

from core.api_request import ApiRequest
from settings import STG

API_PREFIX = "/api/v1.00/public"

class Devices:

    def __init__(self):
        self.host = STG.PILLIGRIMM['url']

    @allure.step('Отправка запроса GET /devices')
    def get_devices(self, token, params, check_ok=True):
        with allure.step(f'GET-запрос на {self.host}{API_PREFIX}/devices'):
            response = ApiRequest(
                url=API_PREFIX + '/devices',
                service_url=self.host,
                method='GET',
                params=params,
                headers={'Authorization': f'Bearer {token}'}
            ).perform(check_ok=check_ok, verify=False)
            return response