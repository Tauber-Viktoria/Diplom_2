import allure

import requests

from helpers import url


class Order:
    @staticmethod
    @allure.step("Создание заказа")
    def create_order(access_token, body_order):
        order_headers = {
            'Accept': 'application/json',
            'Authorization': access_token
        }
        order_response = requests.post(url.CREATE_ORDER, headers=order_headers, json=body_order)
        return order_response

    @staticmethod
    @allure.step("Получение заказа")
    def get_order(access_token):
        order_headers = {
            'Accept': 'application/json',
            'Authorization': access_token
        }
        get_order_response = requests.get(url.GET_USER_ORDER, headers=order_headers)
        return get_order_response
