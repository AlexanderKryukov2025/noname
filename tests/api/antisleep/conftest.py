import pytest
from settings import STG


@pytest.fixture(scope='class')
def get_token(cluster):
    try:
        login_params = {
            "email": STG.ANTISLEEP['login'],
            "password": STG.ANTISLEEP['password']
        }

        response = cluster.login.post_login(params=login_params)
        response.raise_for_status()
        token = response.decoded_body.get('token')
        if not token:
            raise ValueError("Token not found in the response.")

        return token

    except Exception as e:
        pytest.fail(f"Failed to get token: {str(e)}")
