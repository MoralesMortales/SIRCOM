from pathlib import Path
import sys

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))

import sqlite3

from app.database.connect import connectDB

def updateProvider(rif, nombre, direccion, telefono, correo):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE proveedor 
                SET nombreEmpresa = ?, direccionEmpresa = ?, telefono = ?, correo = ?
                WHERE rif = ?
                """,
                (nombre, direccion, telefono, correo, rif),
            )
            connection.commit() 
            return True
        except sqlite3.Error as e:
            print(f"Error updating provider: {e}")
            return False
        finally:
            connection.close()
    return False

def updateProduct(codigo, nombre, precio, stock, minDes, desc, stockMin, estado):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE producto 
                SET nombre = ?, precioUnitario = ?, stock = ?, descuentoDesde = ?, descuento = ?, stockMinimo = ?, estado = ?
                WHERE codigo = ?
                """,
                (nombre, precio, stock, minDes, desc, stockMin, estado, codigo),
            )
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating product: {e}")
            return False
        finally:
            connection.close()
    return False

def updateProductQuantity(codigo, stock):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE producto 
                SET stock = ?
                WHERE codigo = ?
                """,
                (stock, codigo),
            )
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating product: {e}")
            return False
        finally:
            connection.close()
    return False

def updateInventoryProductQuantity(codigo, stock):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE productosInventario 
                SET cantidad = ?
                WHERE codigoProducto = ?
                """,
                (stock, codigo),
            )
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating product: {e}")
            return False
        finally:
            connection.close()
    return False


def updateInventoryProductQuantityMain(codigo, stock):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE productosInventario 
                SET cantidad = ?
                WHERE codigo = ?
                """,
                (stock, codigo),
            )
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating product: {e}")
            return False
        finally:
            connection.close()
    return False

def updateInventoryProductLevels(codigo, stock, min_stock):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE productosInventario SET cantidad = ?, stock_minimo = ? WHERE codigo = ?",
                (stock, min_stock, codigo),
            )
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating levels: {e}")
            return False
        finally:
            connection.close()
    return False

def updateInventoryProductMinStock(codigo, min_stock):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE productosInventario SET stock_minimo = ? WHERE codigo = ?",
                (min_stock, codigo),
            )
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating min stock: {e}")
            return False
        finally:
            connection.close()
    return False
def updateInventoryProductCode(codigo, newCode):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE productosInventario 
                SET codigo = ?
                WHERE codigo = ?
                """,
                (newCode,codigo),
            )
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating product: {e}")
            return False
        finally:
            connection.close()
    return False

def updateHistoryTotalPurchase(codigo, totalPurchase):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE compra 
                SET totalCompra = ?
                WHERE idCompra = ?
                """,
                (totalPurchase,codigo),
            )
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating history: {e}")
            return False
        finally:
            connection.close()
    return False