import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent.parent.parent / ".env"

load_dotenv(env_path)

HOST = os.getenv("HOST")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
CHARSET = os.getenv("CHARSET")


def user_exist():

    connection = None
    connection_cursor = None
    try:
        connection = pymysql.connect(
            host=HOST, user=USERNAME, password=PASSWORD, charset=CHARSET
        )
        connection_cursor = connection.cursor()
        connection_cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = %s AND host = %s)", 
            (USERNAME, HOST)
        )

        user_exists = connection_cursor.fetchone()[0]

        if not user_exists:
            connection_cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '%s' AND host = '%s'), (USERNAME, HOST)"
            )
            print(f"El usuario '{USERNAME}'@'{HOST}' no existe. Creándolo...")
            connection_cursor.execute(
                "CREATE USER %s@%s IDENTIFIED BY '%s';", (USERNAME, HOST, PASSWORD)
            )
            print(f"Usuario '{USERNAME}' creado.")


        else:
            print(f"Usuario '{USERNAME}' ya esta creado.")

    except pymysql.MySQLError as e:
        print(f"Error al configurar la base de datos: {e}")
    finally:
        if connection_cursor:
            connection_cursor.close()
        else:
            print("error B1")
        if connection:
            connection.close()
        else:
            print("error B2")
