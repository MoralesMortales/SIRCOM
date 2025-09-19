import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from app.database.connect import connectDB

def obtener_todos_productos():
    conexion = connectDB()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, stock FROM productos ORDER BY nombre")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            conexion.close()
    return []


def buscar_productos(texto_busqueda):
    conexion = connectDB()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute(
                """
                SELECT id, nombre, stock FROM productos 
                WHERE nombre LIKE ? 
                ORDER BY nombre
            """,
                (f"%{texto_busqueda}%",),
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error en búsqueda: {e}")
            return []
        finally:
            conexion.close()
    return []


def obtener_detalles_producto(producto_id):
    conexion = connectDB()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute(
                """
                SELECT id, nombre, stock, descripcion 
                FROM productos WHERE id = ?
            """,
                (producto_id,),
            )
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener detalles: {e}")
            return None
        finally:
            conexion.close()
    return None
