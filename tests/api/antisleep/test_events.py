import allure
import pytest


@allure.feature("Проверка получения событий")
@allure.tag("BACK")
class TestEvents:

    @allure.title("...")
    @allure.tag("positive")
    def test_events_with_valid_params(self, cluster, get_token):
        params = {
            "page": 1,
            "filter[date_from]": "2025-05-22T00:00:00.000Z",
            "filter[date_to]": "2025-05-22T23:59:59.000Z"
        }
        response = cluster.events.get_events(get_token, params=params).decoded_body
        assert response.status_code == 200


