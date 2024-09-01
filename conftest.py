import pytest
import requests

from api.user import User
from helpers import generation, url


@pytest.fixture
def login():
    data_user = generation.generate_data_user()
    create_response = requests.post(url.CREATE_USER, json=data_user)
    user_access_token = create_response.json().get('accessToken')
    yield data_user

    delete_headers = {
        'Accept': 'application/json',
        'Authorization': user_access_token
    }
    requests.delete(url.DELETE_USER, headers=delete_headers)
