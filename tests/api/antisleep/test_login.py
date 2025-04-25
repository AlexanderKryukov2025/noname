import allure
import pytest


@allure.feature("Проверка аутентификации")
@allure.tag("BACK")
class TestLogin:

    @allure.title("Тест с корректным email и паролем")
    @allure.tag("positive")
    def test_login_with_valid_input(self, cluster):
        payload = {
            "email": "demo@demo.ru",
            "password": "Demo1704@demo.ru"
        }
        response = cluster.login.post_login(params=payload)
        token = response.json()['token']
        assert response.status_code == 200
        assert type(token) == str and token != ''

    @allure.title("Тест с незначительными пробелами перед email и паролем")
    @allure.tag("positive")
    def test_login_with_trimmed_input(self, cluster):
        payload = {
            "email": " demo@demo.ru ",
            "password": " Demo1704@demo.ru "
        }
        response = cluster.login.post_login(params=payload)
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
        payload = {
            "email": email,
            "password": password
        }
        response = cluster.login.post_login(params=payload, check_ok=False)
        assert response.status_code in (401, 422)
        assert response.json()['message'] in (
            'Неверное имя пользователя или пароль.',
            'The email must be a valid email address.',
            'email обязательно к заполнению.',
            'password обязательно к заполнению.')
