from pathlib import Path
import sys

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))

import sqlite3

from app.database.connect import connectDB

def deleteProduct(code):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE producto SET estado = ? WHERE codigo = ?", (0, code,))
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting product: {e}")
            return False
        finally:
            connection.close()
    return False

def deleteProvider(rif):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE proveedor SET estado = ? WHERE rif = ?", (0,rif,))
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting product: {e}")
            return False
        finally:
            connection.close()
    return False

def deleteUser(cedula):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE from usuario WHERE cedula = ?", (cedula,))
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            connection.close()
    return False