import allure

from api.user import User


@allure.feature("Создание пользователя")
class TestCreateCourier:
    @allure.story("Успешное создание уникального пользователя")
    @allure.title("Тест на успешное создание пользователя со всеми полями")
    def test_create_user_successful(self):
        user = User()
        response = user.register_new_user()
        access_token = response.json().get('accessToken')

        assert (response.status_code == 200 and
                response.json()['success'] is True and
                'user' in response.json() and
                'accessToken' in response.json()), \
            f'Статус код {response.status_code},В ответе {response.json()}'

        user.delete_new_user(access_token)

    @allure.story("Ошибка при повторном создании пользователя")
    @allure.title("Попытка создания пользователя с уже существующим логином")
    def test_create_user_repeat_login_error(self):
        user = User()
        response = user.register_new_user()
        email = response.json().get('email')
        access_token = response.json().get('accessToken')

        response = user.register_user_with_email(email)

        assert response.status_code == 403, f'Статус код {response.status_code}'

        user.delete_new_user(access_token)
