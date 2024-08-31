import allure
import pytest
import requests

from helpers import url, generation


class User:
    @allure.step("Создание нового пользователя")
    def register_new_user(self):
        user_data = generation.generate_data_user()

        register_url = url.CREATE_USER
        payload = {
            "email": user_data['email'],
            "password": user_data['password'],
            "name": user_data['first_name']
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(register_url, json=payload, headers=headers)

        if response.status_code == 200:
            return response
        else:
            pytest.fail(f"Ошибка при создании пользователя: {response.status_code} - {response.text}")

    @allure.step("Удаление нового пользователя")
    def delete_new_user(self, access_token):
        delete_url = url.DELETE_USER
        delete_headers = {
            'Accept': 'application/json',
            'Authorization': f'{access_token}'
        }
        delete_response = requests.delete(delete_url, headers=delete_headers)

        if delete_response.status_code != 202:
            pytest.fail(f"Ошибка при удалении пользователя: {delete_response.status_code} - {delete_response.text}")

    @allure.step("Создание пользователя с заданным email")
    def register_user_with_email(self, email):

        register_url = url.CREATE_USER
        payload = {
            "email": email,
            "password": generation.generate_password(),
            "name": generation.generate_first_name()
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(register_url, json=payload, headers=headers)
        return response
