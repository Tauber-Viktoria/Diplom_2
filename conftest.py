import pytest

from api.user import User


@pytest.fixture
def login():
    user = User()
    response = user.register_new_user()
    response_data = response.json()
    access_token = response_data.get('accessToken')
    yield response_data
    user.delete_new_user(access_token)
