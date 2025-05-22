import allure

from core.api_request import ApiRequest
from settings import STG

API_PREFIX = "/api/v1.00/public"


class Login:

    def __init__(self):
        self.host = STG.PILLIGRIMM['url']

    @allure.step('Отправка запроса POST /login')
    def post_login(self, params, check_ok=True):
        with allure.step(f'POST-запрос на {self.host}{API_PREFIX}/login'):
            response = ApiRequest(
                url=API_PREFIX + '/login',
                service_url=self.host,
                method='POST',
                params=params
            ).perform(check_ok=check_ok, verify=False)
            return response

    # @allure.step('Отправка POST-запроса /login с параметрами')
    # def post_login_v2(self, params, payload, check_ok=True):
    #     with allure.step(f'POST-запрос на {self.host}/login'):
    #         response = ApiRequest(
    #             url='/login',
    #             service_url=self.host,
    #             method='POST',
    #             params=params,
    #             json=payload,
    #             # headers={'Cookie': cookie}
    #         ).perform(check_ok=check_ok, verify=False)
    #         return response
