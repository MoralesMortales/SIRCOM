from pathlib import Path
import sys

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))

import sqlite3

from app.database.connect import connectDB

def newUser(cedula, primerNombre, primerApellido, correo, clave):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                insert into usuario (cedula, primerNombre,primerApellido,correo,contrasena) VALUES (?,?,?,?,?)
                """,
                (cedula, primerNombre, primerApellido,correo, clave),
            )
            connection.commit()
            return True
        
        except sqlite3.IntegrityError as e:
            print(f"Error de Integridad (Dato duplicado o nulo): {e}")
            return False       
        
        except sqlite3.Error as e:
            print(f"Error inserting new user: {e}")
            return False
        
        finally:
            connection.close()
