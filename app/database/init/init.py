from .database_exist import database_exist

def initialize_db():
    try:
        database_exist()

    except Exception as e:
        print(f"Error {e}")
        raise e


