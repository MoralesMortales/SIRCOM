from pathlib import Path
import sys

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))

import sqlite3

from app.database.connect import connectDB

def authData(cedula, clave):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT cedula, contrasena 
                FROM usuario WHERE (cedula, contrasena) = (?,?)
                """,
                (cedula, clave),
            )
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener detalles: {e}")
            return None
        finally:
            connection.close()

def authCedula(cedula):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT primerNombre 
                FROM usuario WHERE (cedula) = (?)
                """,
                (cedula,),
            )
            user = cursor.fetchone()
            print(user)
            return user
        except sqlite3.Error as e:
            print(f"Error al obtener detalles: {e}")
            return None
        finally:
            connection.close()