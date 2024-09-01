class MassageUser:
    USER_ALREADY_EXISTS = 'User already exists'
    EMAIL_PASSWORD_NAME_REQUIRED = 'Email, password and name are required fields'
    EMAIL_PASSWORD_INCORRECT = 'email or password are incorrect'
    WITHOUT_AUTHORIZATION = 'You should be authorised'


class MassageOrder:
    WITHOUT_INGREDIENT = 'Ingredient ids must be provided'
    INTERNAL_SERVER_ERROR = ('<!DOCTYPE html><html lang="en"><head><meta '
                             'charset="utf-8"><title>Error</title></head><body><pre>Internal Server '
                             'Error</pre></body></html>')
