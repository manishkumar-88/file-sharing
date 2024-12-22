from configs import settings
from mongoengine import *
import logging


def initialize_db():
    try:
        url = f'mongodb://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}'
        if settings.db_host == 'localhost':
            url = f'mongodb://localhost/{settings.db_name}'
        connect(    
            host=url
        )
    except Exception as ex:
        print(ex)

def close_db():
    try:
        disconnect()
    except Exception as ex:
        print(f"Error disconnecting from the database: {ex}")