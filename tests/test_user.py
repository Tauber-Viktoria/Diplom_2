import allure
import pytest

from api.user import User
from helpers import generation
from helpers.message import MassageUser


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
    @allure.title("Тест на создание пользователя с уже существующим логином")
    def test_create_user_repeat_login_error(self, create_and_delete_user):
        data_user = create_and_delete_user
        response = User.register_new_user(data_user)

        assert (response.status_code == 403 and
                response.json()['success'] is False and
                response.json().get('message') == MassageUser.USER_ALREADY_EXISTS), \
            f'Статус код {response.status_code},В ответе {response.json()}'

    @allure.story("Ошибка при создании учетной записи курьера без обязательных полей")
    @allure.title("Тест на создание учетной записи курьера без обязательного поля")
    @pytest.mark.parametrize("data_user", [
        (generation.generate_data_user(include_first_name=False)),
        (generation.generate_data_user(include_email=False)),
        (generation.generate_data_user(include_password=False)),
    ])
    def test_create_user_no_required_field_error(self, data_user):
        response = User.register_new_user(data_user)

        assert (response.status_code == 403 and
                response.json()['success'] is False and
                response.json().get('message') == MassageUser.EMAIL_PASSWORD_NAME_REQUIRED), \
            f'Статус код {response.status_code},В ответе {response.json()}'


@allure.feature("Авторизация пользователя")
class TestLoginUser:
    @allure.story("Успешная авторизация пользователя")
    @allure.title("Тест на авторизацию пользователя при передаче всех обязательных полей")
    def test_login_user_successful(self, create_and_delete_user):
        data_user = create_and_delete_user
        login_response = User.login_user(data_user.get('email', ''), data_user.get('password', ''))
        access_token = login_response.json().get('accessToken')
        assert (login_response.status_code == 200 and
                login_response.json()['success'] is True and
                'user' in login_response.json() and
                access_token), \
            f"Статус код {login_response.status_code}, В ответе {login_response.json()}"

    @allure.story("Ошибка если неправильно указать логин или пароль")
    @allure.title("Тест на авторизацию с заменой значения у обязательного поля")
    @pytest.mark.parametrize("error_value", ["email", "password"])
    def test_login_user_invalid_value_error(self, create_and_delete_user, error_value):
        data_user = create_and_delete_user.copy()
        email = data_user.get('email', '')
        password = data_user.get('password', '')

        if error_value == "email":
            data_user['email'] = 'errorERRORerror666@mail.com'
        elif error_value == "password":
            data_user['password'] = 'errorERRORerror666'

        login_response = User.login_user(data_user.get('email', email), data_user.get('password', password))

        assert (login_response.status_code == 401 and
                login_response.json()['success'] is False and
                login_response.json().get('message') == MassageUser.EMAIL_PASSWORD_INCORRECT), \
            f'Статус код {login_response.status_code},В ответе {login_response.json()}'


@allure.feature("Изменения данных пользователя")
class TestChangeUserData:
    @allure.story("Успешное изменение данных пользователя")
    @allure.title("Тест на изменение данных пользователя с авторизацией")
    @pytest.mark.parametrize("value", ["email", "name"])
    def test_change_user_data_successful(self, create_and_delete_user, value):
        data_user = create_and_delete_user
        email = data_user.get('email', '')
        password = data_user.get('password', '')
        login_response = User.login_user(data_user.get('email', email), data_user.get('password', password))
        access_token = login_response.json().get('accessToken')

        updated_data = data_user.copy()
        if value == "email":
            updated_data['email'] = "newemail123@mail.com"
        elif value == "name":
            updated_data['name'] = "NewUsername123"

        change_response = User.change_user_data(access_token, updated_data)
        assert (change_response.status_code == 200 and
                change_response.json()['success'] is True and
                'user' in change_response.json()), \
            f'Статус код {change_response.status_code}, В ответе {change_response.json()}'

    @allure.story("Ошибка при изменении данных пользователя")
    @allure.title("Тест на изменение данных пользователя без авторизации")
    @pytest.mark.parametrize("value", ["email", "name"])
    def test_change_user_data_without_authorization_error(self, create_and_delete_user, value):
        data_user = create_and_delete_user
        email = data_user.get('email', '')
        password = data_user.get('password', '')
        User.login_user(data_user.get('email', email), data_user.get('password', password))
        access_token = None

        updated_data = data_user.copy()
        if value == "email":
            updated_data['email'] = "newemail123@mail.com"
        elif value == "name":
            updated_data['name'] = "NewUsername123"

        change_response = User.change_user_data(access_token, updated_data)
        assert (change_response.status_code == 401 and
                change_response.json()['success'] is False and
                change_response.json().get('message') == MassageUser.WITHOUT_AUTHORIZATION), \
            f'Статус код {change_response.status_code}, В ответе {change_response.json()}'
