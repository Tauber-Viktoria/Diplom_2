import allure
import pytest
import requests
from helpers import url
from helpers.generete import generate_data_user


class RegisterUser:
    @allure.step("Создание нового пользователя")
    def register_new_user(self):
        user_data = generate_data_user()

        register_url = url.CREATE_USER
        payload = {
            "email": user_data['email'],
            "password": user_data['password'],
            "name": user_data['first_name']
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(register_url, json=payload, headers=headers)

        if response.status_code == 200:
            user_data['access_token'] = response.json().get("accessToken")
            return user_data, response
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
