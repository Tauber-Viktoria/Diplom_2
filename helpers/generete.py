from faker import Faker

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


def generate_data_user():
    data_user = {
        'first_name': generate_first_name(),
        'email': generate_email(),
        'password': generate_password()
    }
    return data_user
