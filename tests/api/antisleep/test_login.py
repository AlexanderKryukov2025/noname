import allure
import pytest


@allure.feature("Проверка аутентификации")
@allure.tag("BACK")
class TestLogin:

    @allure.title("Тест с корректным email и паролем")
    @allure.tag("positive")
    def test_login_with_valid_input(self, cluster):
        params = {
            "email": "demo@demo.ru",
            "password": "Demo1704@demo.ru"
        }
        response = cluster.login.post_login(params=params)
        token = response.json()['token']
        assert response.status_code == 200
        assert type(token) == str and token != ''

    @allure.title("Тест с незначительными пробелами перед email и паролем")
    @allure.tag("positive")
    def test_login_with_trimmed_input(self, cluster):
        params = {
            "email": " demo@demo.ru ",
            "password": " Demo1704@demo.ru "
        }
        response = cluster.login.post_login(params=params)
        assert response.status_code == 200

    @allure.title("Тест с некорректным email")
    @allure.tag("negative")
    @pytest.mark.parametrize("email, password", [
        ("", "Demo1704@demo.ru"),  # Путой имейл
        ("demo@demo.ru", ""),  # Пустой пароль
        ("demo@demo", "Demo1704@demo.ru"),  # Отсутствует домен имейла
        ("@demo.ru", "Demo1704@demo.ru"),  # Отсутствует локальная часть имейла
        ("demo@", "Demo1704@demo.ru"),  # Отсутствует доменное имя имейла
        ("demo@.com", "Demo1704@demo.ru"),  # Некорректный домен имейла
        ("demo@demo..ru", "Demo1704@demo.ru"),  # Две точки подряд в доменном имени имейла
        ("demo@-demo.ru", "Demo1704@demo.ru"),  # Начало с тире в домене имейла
        # ... перечислить тоже самое с паролем
    ])
    def test_login_invalid_email_format(self, cluster, email, password):
        params = {
            "email": email,
            "password": password
        }
        response = cluster.login.post_login(params=params, check_ok=False)
        assert response.status_code in (401, 422)
        assert response.json()['message'] in (
            'Неверное имя пользователя или пароль.',
            'The email must be a valid email address.',
            'email обязательно к заполнению.',
            'password обязательно к заполнению.')



    # @allure.title("Тест с корректным email и паролем")
    # @allure.tag("positive")
    # def test_123(self, cluster):
    #     payload = {
    #         "email": "a.krukov@antisleep.ru",
    #         "password": "Kryukov1988.",
    #     }
    #     token = cluster.login.post_login(params=payload).decoded_body['token']
    #     token_target = token.split('.')[1]
    #     payload = {
    #         "email": "a.krukov@antisleep.ru",
    #         "password": "Kryukov1988.",
    #         "_token": "txAXfudxIf3m3Ajb2dFlTmOUfLJ0KN9zrI3qUyLH",
    #         "action": "logon",
    #         "back": "/"
    #     }
    #     cookie = {f'XSRF-TOKEN={token_target}'}
    #     params = {"language": "ru"}
    #     from settings import STG
    #     cluster.login.host = STG.MGT['url']
    #     # response = cluster.login.post_login_v2(params=params, payload=payload, cookie=cookie)
    #     response = cluster.login.post_login_v2(params=params, payload=payload)
    #     token = response.json()['token']
    #     assert response.status_code == 200
    #     assert type(token) == str and token != ''