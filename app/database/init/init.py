import pymysql
from .database_exist import database_exist
from .user_exist import user_exist

def initialize_db():
    user_exist()
    database_exist()


