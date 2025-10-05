import sqlite3
from app.database.connect import connectDB

def getAllProducts():
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, nombre, stock FROM productos ORDER BY nombre")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            connection.close()
    return []


def searchProducts(text_search):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, nombre, stock FROM productos 
                WHERE nombre LIKE ? 
                ORDER BY nombre
            """,
                (f"%{text_search}%",),
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error en búsqueda: {e}")
            return []
        finally:
            connection.close()
    return []


def getDetatilsProduct(product_id):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, nombre, stock, descripcion 
                FROM productos WHERE id = ?
            """,
                (product_id,),
            )
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener detalles: {e}")
            return None
        finally:
            connection.close()
    return None
