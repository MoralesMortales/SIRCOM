import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv

from database.init.create_tables import create_tables

def database_exist():
    env_path = Path(__file__).parent.parent.parent.parent / ".env"

    # if not env_path.exists():
    #     print(f"Error: .env file not found at {env_path}")
    #     return False

    load_dotenv(env_path)

    HOST = os.getenv("HOST")
    USERNAME = os.getenv("USERNAME")
    DATABASE = os.getenv("DATABASE")
    PASSWORD = os.getenv("PASSWORD")
    CHARSET = os.getenv("CHARSET")

    connection = None
    connection_cursor = None

    try:

        connection = pymysql.connect(
            host=HOST, user=USERNAME, password=PASSWORD, charset=CHARSET
        )

        connection_cursor = connection.cursor()

        connection_cursor.execute("SHOW DATABASES;")
        databases = [db[0] for db in connection_cursor.fetchall()]

        if "inventory_database" not in databases:
            print(f"La base de datos '{DATABASE}' no existe. Creándola...")

            connection_cursor.execute(f"CREATE DATABASE {DATABASE};")
            print(f"La base de datos '{DATABASE}' ha sido creada.")

            connection_cursor.execute(f"GRANT ALL PRIVILEGES ON {DATABASE}.* TO %s@%s IDENTIFIED BY %s;", 
                (USERNAME, HOST, PASSWORD)
            )
            connection_cursor.execute("FLUSH PRIVILEGES;")
            connection.commit()

            create_tables()

        else:
            print(f"La base de datos '{DATABASE}' ya existe.")

    except pymysql.MySQLError as e:
        print(f"Error al configurar la base de datos: {e}")

    finally:
        if connection_cursor:
            connection_cursor.close()
        else:
            print("error A1")

        if connection:
            connection.close()
        else:
            print("error A2")
