import os

# CONFIG SECTION
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REGISTERED_USERS = {
        'charliesaleh@outlook.com': {
            'name': 'Charlie Saleh',
            'password': 'nicetrynotgonnagiveoutmypassword'
        },
    }
