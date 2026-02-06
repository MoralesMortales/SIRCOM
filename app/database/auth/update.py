from pathlib import Path
import sys

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))

import sqlite3

from app.database.connect import connectDB
def updatePurchaseStatus(purchase_id, status):
    """Actualiza el estado de una compra"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE compra SET estado = ? WHERE idCompra = ?",
                (status, purchase_id)
            )
            connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating purchase status: {e}")
            return False
        finally:
            connection.close()
    return False

def updateProductStock(product_code, new_stock):
    """Actualiza el stock de un producto"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE producto SET stock = ? WHERE codigo = ?",
                (new_stock, product_code)
            )
            connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating product stock: {e}")
            return False
        finally:
            connection.close()
    return False
def updateProduct(nombre, precioUnitario, stock, stockMinimo, descripcion, rifProveedor, codigo, descuentoDesde=0, descuento=0):
    """Actualiza un producto existente en la base de datos"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Verificar si el producto existe
            cursor.execute(
                "SELECT codigo FROM producto WHERE codigo = ? AND rifProveedor = ?",
                (codigo, rifProveedor)
            )
            if not cursor.fetchone():
                return False  # Producto no existe
            
            # Actualizar el producto - ORDEN CORREGIDO
            cursor.execute("""
                UPDATE producto 
                SET nombre = ?, 
                    precioUnitario = ?, 
                    stock = ?, 
                    stockMinimo = ?, 
                    descripcion = ?,
                    descuentoDesde = ?,
                    descuento = ?
                WHERE codigo = ? AND rifProveedor = ?
            """, (nombre, precioUnitario, stock, stockMinimo, descripcion, 
                  descuentoDesde, descuento, codigo, rifProveedor))
            
            connection.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Error updating product: {e}")
            return False
        finally:
            connection.close()
    return False
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