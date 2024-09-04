import random

from faker import Faker

from helpers.data import ingredients

fake = Faker("ru_RU")


def generate_first_name():
    first_name = fake.first_name()
    return first_name


def generate_email():
    email = fake.email()
    return email


def generate_password():
    password = fake.password()
    return password


def generate_data_user(include_first_name=True, include_email=True, include_password=True):
    data_user = {}
    if include_first_name:
        data_user['name'] = generate_first_name()
    if include_email:
        data_user['email'] = generate_email()
    if include_password:
        data_user['password'] = generate_password()

    return data_user


def generate_body_order():
    buns = [item for item in ingredients if item['type'] == 'bun']
    others = [item for item in ingredients if item['type'] != 'bun']

    bun = random.choice(buns)

    other_count = random.randint(1, 14)
    selected_others = random.sample(others, other_count)

    selected_ingredients = [bun['_id']] + [item['_id'] for item in selected_others]

    body_order = {"ingredients": selected_ingredients}

    return body_order
