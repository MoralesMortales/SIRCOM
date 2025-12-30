import sqlite3
from app.database.connect import connectDB

def getAllProducts():
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT p.descuento, p.descuentoDesde, p.codigo, p.nombre AS nombreProducto, pr.nombreEmpresa, p.stock, p.stockMinimo, p.precioUnitario AS nombreProveedor FROM producto p JOIN proveedor pr ON p.rifProveedor = pr.rif WHERE pr.estado = 1 AND p.estado = 1;")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting products: {e}")
            return []
        finally:
            connection.close()
    return []


                