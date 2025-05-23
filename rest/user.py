import allure

from core.api_request import ApiRequest
from settings import STG

API_PREFIX = "/api/v1.00/public"

class User:

    def __init__(self):
        self.host = STG.PILLIGRIMM['url']

    @allure.step('Отправка запроса GET /user')
    def get_user(self, token, check_ok=True):
        with allure.step(f'GET-запрос на {self.host}{API_PREFIX}/user'):
            response = ApiRequest(
                url=API_PREFIX + '/user',
                service_url=self.host,
                method='GET',
                headers={'Authorization': f'Bearer {token}'}
            ).perform(check_ok=check_ok, verify=False)
            return response