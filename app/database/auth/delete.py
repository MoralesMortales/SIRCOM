from pathlib import Path
import sys

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))

import sqlite3

from app.database.connect import connectDB

def deletePurchase(purchase_id):
    """Elimina una compra y sus detalles"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Primero, restaurar el stock de los productos
            cursor.execute(
                """
                SELECT dc.codigoProducto, dc.cantidad, p.stock
                FROM detalleCompra dc
                JOIN producto p ON dc.codigoProducto = p.codigo
                WHERE dc.idCompra = ?
                """,
                (purchase_id,)
            )
            
            products = cursor.fetchall()
            
            # Restaurar stock para cada producto
            for product_code, cantidad, stock_actual in products:
                nuevo_stock = int(stock_actual) + int(cantidad)
                cursor.execute(
                    "UPDATE producto SET stock = ? WHERE codigo = ?",
                    (nuevo_stock, product_code)
                )
            
            # Eliminar detalles de compra
            cursor.execute(
                "DELETE FROM detalleCompra WHERE idCompra = ?",
                (purchase_id,)
            )
            
            # Eliminar la compra
            cursor.execute(
                "DELETE FROM compra WHERE idCompra = ?",
                (purchase_id,)
            )
            
            connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting purchase: {e}")
            connection.rollback()
            return False
        finally:
            connection.close()
    return False

def cancelPurchase(purchase_id):
    """Cancela una compra cambiando su estado a 'Cancelado'"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Restaurar stock de productos
            cursor.execute(
                """
                SELECT dc.codigoProducto, dc.cantidad, p.stock
                FROM detalleCompra dc
                JOIN producto p ON dc.codigoProducto = p.codigo
                WHERE dc.idCompra = ?
                """,
                (purchase_id,)
            )
            
            products = cursor.fetchall()
            
            for product_code, cantidad, stock_actual in products:
                nuevo_stock = int(stock_actual) + int(cantidad)
                cursor.execute(
                    "UPDATE producto SET stock = ? WHERE codigo = ?",
                    (nuevo_stock, product_code)
                )
            
            # Cambiar estado a Cancelado
            cursor.execute(
                "UPDATE compra SET estado = 'Cancelado' WHERE idCompra = ?",
                (purchase_id,)
            )
            
            connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error cancelling purchase: {e}")
            connection.rollback()
            return False
        finally:
            connection.close()
    return False

def deleteProduct(codigo):
    """Elimina un producto de un proveedor"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM producto WHERE codigo = ?",
                (codigo,)
            )
            connection.commit()
            return cursor.rowcount > 0
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