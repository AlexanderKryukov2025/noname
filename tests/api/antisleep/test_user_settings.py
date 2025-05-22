import allure


@allure.feature("Проверка настроек пользователя")
@allure.tag("BACK")
class TestUserSettings:

    # Позитивные тесты
    @allure.tag("positive")
    def test_update_user_settings_valid_name(self, cluster, get_token):
        params = {
            "name": "New Name",
            "time_zone": "Asia/Yakutsk",
            "sip_number": "12345",
            "sip_extension": "67890",
            "events_view_type": 1,
            "locale": "en"
        }
        response = cluster.user_settings.put_settings(get_token, params=params)
        # тут нужен запрос к БД чтобы проверить изменение пользователя оттуда сопоставив результаты из БД с payload
        assert response.status_code == 200
        assert response.text == '{"success":true}'

    @allure.tag("positive")
    def test_update_user_settings_valid_time_zone(self, cluster, get_token):
        params = {
            "name": "User",
            "time_zone": "Europe/Moscow",
            "sip_number": "12345",
            "sip_extension": "67890",
            "events_view_type": 2,
            "locale": "en"
        }
        response = cluster.user_settings.put_settings(get_token, params=params)
        assert response.status_code == 200
        assert response.text == '{"success":true}'

    # Негативные тесты
    @allure.tag("negative")
    def test_update_user_settings_missing_name(self, cluster, get_token):
        params = {
            "time_zone": "Asia/Yakutsk",
            "sip_number": "12345",
            "sip_extension": "67890",
            "events_view_type": 1,
            "locale": "en"
        }
        response = cluster.user_settings.put_settings(get_token, params=params, check_ok=False)
        assert response.status_code == 422
        assert response.decoded_body['message'] == 'Имя и фамилия обязательно к заполнению.'

    @allure.tag("negative")
    def test_update_user_settings_missing_time_zone(self, cluster, get_token):
        params = {
            "name": "User",
            "sip_number": "12345",
            "sip_extension": "67890",
            "events_view_type": 1,
            "locale": "en"
        }
        response = cluster.user_settings.put_settings(get_token, params=params, check_ok=False)
        assert response.status_code == 422
        assert response.decoded_body['message'] == 'Часовой пояс пользователя обязательно к заполнению.'

    @allure.tag("negative")
    def test_update_user_settings_missing_events_view_type(self, cluster, get_token):
        params = {
            "name": "User",
            "time_zone": "Asia/Yakutsk",
            "sip_number": "12345",
            "sip_extension": "67890",
            "locale": "en"
        }
        response = cluster.user_settings.put_settings(get_token, params=params, check_ok=False)
        assert response.status_code == 422
        assert response.decoded_body['message'] == 'Способ отображения списков событий обязательно к заполнению.'

    @allure.tag("negative")
    def test_update_user_settings_empty_name(self, cluster, get_token):
        params = {
            "name": "",
            "time_zone": "Asia/Yakutsk",
            "sip_number": "12345",
            "sip_extension": "67890",
            "events_view_type": 1,
            "locale": "en"
        }
        response = cluster.user_settings.put_settings(get_token, params=params, check_ok=False)
        assert response.status_code == 422
        assert response.decoded_body['message'] == 'Имя и фамилия обязательно к заполнению.'

    @allure.tag("negative")
    def test_update_user_settings_invalid_time_zone(self, cluster, get_token):
        params = {
            "name": "User",
            "time_zone": "Invalid/FakeZone",
            "sip_number": "12345",
            "sip_extension": "67890",
            "events_view_type": 1,
            "locale": "en"
        }
        response = cluster.user_settings.put_settings(get_token, params=params, check_ok=False)
        assert response.status_code == 422
        assert response.decoded_body['message'] == '...'  # Недопустимая таймзона

    @allure.tag("negative")
    def test_update_user_settings_null_events_view_type(self, cluster, get_token):
        params = {
            "name": "User",
            "time_zone": "Asia/Yakutsk",
            "sip_number": "12345",
            "sip_extension": "67890",
            "events_view_type": None,
            "locale": "en"
        }
        response = cluster.user_settings.put_settings(get_token, params=params, check_ok=False)
        assert response.status_code == 422
        assert response.decoded_body['message'] == 'Способ отображения списков событий обязательно к заполнению.'
