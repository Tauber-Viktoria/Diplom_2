import allure
import pytest

from api.user import User
from helpers import generation
from helpers.message import EMAIL_PASSWORD_NAME_REQUIRED


@allure.feature("Создание пользователя")
class TestCreateCourier:
    @allure.story("Успешное создание уникального пользователя")
    @allure.title("Тест на успешное создание пользователя со всеми полями")
    def test_create_user_successful(self):
        data_user = generation.generate_data_user()
        response = User.register_new_user(data_user)
        access_token = response.json().get('accessToken')

        assert (response.status_code == 200 and
                response.json()['success'] is True and
                'user' in response.json() and
                'accessToken' in response.json()), \
            f'Статус код {response.status_code},В ответе {response.json()}'

        User.delete_new_user(access_token)

    @allure.story("Ошибка при повторном создании пользователя")
    @allure.title("Попытка создания пользователя с уже существующим логином")
    def test_create_user_repeat_login_error(self):
        data_user = generation.generate_data_user()
        response = User.register_new_user(data_user)
        email = response.json().get('email')
        access_token = response.json().get('accessToken')

        response = User.register_user_with_email(email)

        assert response.status_code == 403, f'Статус код {response.status_code}'

        User.delete_new_user(access_token)

    @allure.story("Ошибка при создании учетной записи курьера без обязательных полей")
    @allure.title("Создание учетной записи курьера без обязательного поля")
    @pytest.mark.parametrize("data_user, expected_status_code, expected_response", [
        # Поле first_name отсутствует
        (generation.generate_data_user(include_first_name=False), 403, EMAIL_PASSWORD_NAME_REQUIRED),
        # Поле email отсутствует
        (generation.generate_data_user(include_email=False), 403, EMAIL_PASSWORD_NAME_REQUIRED),
        # Поле password отсутствует
        (generation.generate_data_user(include_password=False), 403, EMAIL_PASSWORD_NAME_REQUIRED),
    ])
    def test_create_user_no_required_field_error(self, data_user, expected_status_code, expected_response):
        response = User.register_new_user(data_user)

        assert (response.status_code == expected_status_code
                and response.json().get('message') == expected_response), \
            f'Статус код {response.status_code},В ответе {response.json()}'

