import pytest

from api.register_user import RegisterUser


@pytest.fixture
def login():
    user_data, response = RegisterUser.register_new_user()  # Регистрация нового пользователя
    yield user_data
    access_token = user_data.get('access_token')
    RegisterUser.delete_new_user(access_token)  # Вызов функции удаления пользователя
