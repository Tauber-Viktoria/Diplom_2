import allure

from api.orders import Order
from api.user import User
from helpers.generation import generate_body_order
from helpers.message import MassageOrder


@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.story("Успешное создание заказа с авторизацией и с ингридиентами")
    @allure.title("Тест на создание заказа с авторизацией и с ингридиентами")
    def test_create_order_successful(self, login_in):
        access_token = login_in.json().get('accessToken')
        body_order = generate_body_order()

        order_response = Order.create_order(access_token, body_order)
        assert (order_response.status_code == 200 and
                order_response.json()['success'] is True and
                'order' in order_response.json()), \
            f'Статус код {order_response.status_code}, В ответе {order_response.json()}'

    @allure.story("Ошибка при создании заказа без авторизации")
    @allure.title("Тест на создание заказа без авторизации")
    def test_create_order_without_authorization_error(self, create_and_delete_user):
        data_user = create_and_delete_user
        email = data_user.get('email', '')
        password = data_user.get('password', '')
        User.login_user(data_user.get('email', email), data_user.get('password', password))
        access_token = None
        body_order = generate_body_order()

        order_response = Order.create_order(access_token, body_order)
        assert (order_response.status_code == 200 and
                order_response.json()['success'] is True and
                'order' in order_response.json()), \
            f'Статус код {order_response.status_code}, В ответе {order_response.json()}'

    @allure.story("Ошибка при создании заказа с авторизацией без ингридиентов")
    @allure.title("Тест на создание заказа с авторизацией без ингридиентов")
    def test_create_order_without_ingredient_error(self, login_in):
        access_token = login_in.json().get('accessToken')
        body_order = None

        order_response = Order.create_order(access_token, body_order)
        assert (order_response.status_code == 400 and
                order_response.json().get('message') == MassageOrder.WITHOUT_INGREDIENT and
                order_response.json()['success'] is False), \
            f'Статус код {order_response.status_code}, В ответе {order_response.json()}'

    @allure.story("Ошибка при создании заказа с авторизацией с неверным хешем ингредиентов")
    @allure.title("Тест на создание заказа с авторизацией с неверным хешем ингредиентов")
    def test_create_order_incorrect_ingredient_error(self, login_in):
        access_token = login_in.json().get('accessToken')
        body_order = {"ingredients": ["61c0c5a71d1f82001bdaaa73232321", "61c0c5a71d1f82001bdaaa6c233232"]}

        order_response = Order.create_order(access_token, body_order)
        assert order_response.status_code == 500, \
            f'Статус код {order_response.status_code}'
