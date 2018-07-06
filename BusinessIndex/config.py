import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Hello, my name is Rudolf and I have a secret...'
    ITEMS_PER_PAGE = 20
    MAX_ITEMS_RETURNED = 2000

