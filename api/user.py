import allure
import pytest
import requests

from helpers import url, generation


class User:
    @staticmethod
    @allure.step("Создание нового пользователя")
    def register_new_user(data_user):
        response = requests.post(url.CREATE_USER, json=data_user)
        return response

    @staticmethod
    @allure.step("Удаление нового пользователя")
    def delete_new_user(access_token):
        delete_headers = {
            'Accept': 'application/json',
            'Authorization': f'{access_token}'
        }
        delete_response = requests.delete(url.DELETE_USER, headers=delete_headers)

        if delete_response.status_code != 202:
            pytest.fail(f"Ошибка при удалении пользователя: {delete_response.status_code} - {delete_response.text}")

