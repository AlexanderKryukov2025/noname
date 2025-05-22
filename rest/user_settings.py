import allure

from core.api_request import ApiRequest
from settings import STG

API_PREFIX = "/api/v1.00/public"


class UserSettings:

    def __init__(self):
        self.host = STG.ANTISLEEP['url']

    @allure.step('Отправка запроса PUT /login')
    def put_settings(self, token, params, check_ok=True):
        with allure.step(f'PUT-запрос на {self.host}{API_PREFIX}/user/settings'):
            response = ApiRequest(
                url=API_PREFIX + '/user/settings',
                service_url=self.host,
                method='PUT',
                params=params,
                headers={'Authorization': f'Bearer {token}'}
            ).perform(check_ok=check_ok, verify=False)
            return response
