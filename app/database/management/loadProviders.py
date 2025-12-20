import sqlite3
from app.database.connect import connectDB

def getAllProviders():
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT rif, nombreEmpresa, direccionEmpresa, telefono, correo FROM proveedor WHERE estado = 1")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting providers: {e}")
            return []
        finally:
            connection.close()
    return []
