import os

# CONFIG SECTION
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REGISTERED_USERS = {
        'charliesaleh@outlook.com': {
            'name': 'Charlie Saleh',
            'password': 'nicetrynotgonnagiveoutmypassword'
        },
        'christianskew@thieves.com': {
            'name': 'Christian Askew',
            'password': 'ilovemycoding'
        },
        'dylankatina@thieves.com': {
            'name': 'Dylan Katina',
            'password': 'ilovemydog'
        }
    }
    
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UNREGISTERED_USERS = {
        
    }
