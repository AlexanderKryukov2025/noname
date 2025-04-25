import allure

from core.api_request import ApiRequest
from settings import STG


class Login:

    def __init__(self):
        self.host = STG.ANTISLEEP['host']

    @allure.step('Отправка запроса post /login')
    def post_login(self, params, check_ok=True):
        with allure.step(f'POST-запрос на {self.host}/api/v1.00/public/login'):
            response = ApiRequest(
                url='/api/v1.00/public/login',
                service_url=self.host,
                method='POST',
                params=params
            ).perform(check_ok=check_ok, verify=False)
            return response
