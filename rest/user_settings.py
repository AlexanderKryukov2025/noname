import allure

from core.api_request import ApiRequest
from settings import STG


class UserSettings:

    def __init__(self):
        self.host = STG.ANTISLEEP['url']

    @allure.step('Отправка запроса put /login')
    def put_settings(self, token, params, check_ok=True):
        with allure.step(f'PUT-запрос на {self.host}/api/v1.00/public/user/settings'):
            response = ApiRequest(
                url='/api/v1.00/public/user/settings',
                service_url=self.host,
                method='PUT',
                params=params,
                headers={'Authorization': f'Bearer {token}'}
            ).perform(check_ok=check_ok, verify=False)
            return response
