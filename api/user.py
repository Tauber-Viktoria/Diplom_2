import allure
import pytest
import requests

from helpers import url


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

    @staticmethod
    @allure.step("Логин пользователя")
    def login_user(login, password):
        login_response = requests.post(url.LOGIN_USER, json={'email': login, 'password': password})
        return login_response

    @staticmethod
    @allure.step("Изменить данные пользователя")
    def change_user_data(access_token, updated_data):
        change_headers = {
            'Accept': 'application/json',
            'Authorization': f'{access_token}'
        }
        change_response = requests.patch(url.CHANGE_USER_DATA, headers=change_headers, json=updated_data)
        return change_response
