import allure

import requests

from helpers import url


class Order:
    @staticmethod
    @allure.step("Создание заказа")
    def create_order(access_token, body_order):
        order_headers = {
            'Accept': 'application/json',
            'Authorization': f'{access_token}'
        }
        order_response = requests.post(url.CREATE_ORDER, headers=order_headers, json=body_order)
        return order_response
