from pathlib import Path
import sys

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))

import sqlite3

from app.database.connect import connectDB

def getPendingPurchases():
    """Obtiene todas las compras con estado 'En Curso'"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT idCompra, totalCompra, fechaCompra, nombreUsuario, estado
                FROM compra 
                WHERE estado = 'En Curso'
                ORDER BY fechaCompra DESC
                """
            )
            purchases = cursor.fetchall()
            return purchases
        except sqlite3.Error as e:
            print(f"Error getting pending purchases: {e}")
            return []
        finally:
            connection.close()
    return []

def getPurchaseDetails(purchase_id):
    """Obtiene los detalles de una compra específica"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT 
                    dc.codigoProducto,
                    p.nombre as nombre_producto,
                    p.descripcion,
                    pr.rif,
                    pr.nombreEmpresa as proveedor,
                    dc.cantidad,
                    dc.precioUnitario,
                    dc.subTotal,
                    p.stockMinimo,
                    p.descuento,
                    p.descuentoDesde,
                FROM detalleCompra dc
                JOIN producto p ON dc.codigoProducto = p.codigo
                JOIN proveedor pr ON p.rifProveedor = pr.rif
                WHERE dc.idCompra = ?
                """,
                (purchase_id,)
            )
            details = cursor.fetchall()
            
            # Convertir a lista de diccionarios para mejor manejo
            result = []
            for row in details:
                result.append({
                    'codigo_producto': row[0],
                    'nombre_producto': row[1],
                    'descripcion': row[2],
                    'rif': row[3],
                    'proveedor': row[4],
                    'cantidad': row[5],
                    'precio_unitario': row[6],
                    'total': row[7],
                    'stock_minimo': row[8],
                    'descuento': row[9],
                    'descuento_desde': row[10]
                })
            return result
        except sqlite3.Error as e:
            print(f"Error getting purchase details: {e}")
            return []
        finally:
            connection.close()
    return []

def getPurchaseStatus(purchase_id):
    """Obtiene el estado de una compra específica"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT estado FROM compra WHERE idCompra = ?",
                (purchase_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error getting purchase status: {e}")
            return None
        finally:
            connection.close()
    return None
def getAllComprasWithStatus():
    """Obtiene todas las compras con su estado"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT idCompra, nombreUsuario, fechaCompra, totalCompra, estado
                FROM compra 
                ORDER BY fechaCompra DESC
                """
            )
            data = cursor.fetchall()
            return data 
        except sqlite3.Error as e:
            print(f"Error getting purchases with status: {e}")
            return None
        finally:
            connection.close()

def getComprasByStatus(status):
    """Obtiene compras filtradas por estado"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT idCompra, nombreUsuario, fechaCompra, totalCompra, estado
                FROM compra 
                WHERE estado = ?
                ORDER BY fechaCompra DESC
                """,
                (status,)
            )
            data = cursor.fetchall()
            return data 
        except sqlite3.Error as e:
            print(f"Error getting purchases by status: {e}")
            return None
        finally:
            connection.close()
def getPurchaseById(purchase_id):
    """Obtiene información completa de una compra"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT idCompra, totalCompra, fechaCompra, nombreUsuario, estado
                FROM compra 
                WHERE idCompra = ?
                """,
                (purchase_id,)
            )
            purchase = cursor.fetchone()
            
            if purchase:
                return {
                    'id': purchase[0],
                    'total': purchase[1],
                    'fecha': purchase[2],
                    'usuario': purchase[3],
                    'estado': purchase[4]
                }
            return None
        except sqlite3.Error as e:
            print(f"Error getting purchase by id: {e}")
            return None
        finally:
            connection.close()
    return None
def checkProductExists(codigo, rifProveedor):
    """Verifica si un producto ya existe para un proveedor"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT codigo FROM producto WHERE codigo = ? AND rifProveedor = ?",
                (codigo, rifProveedor)
            )
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Error checking product existence: {e}")
            return False
        finally:
            connection.close()
    return False
def getEmail(cedula):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT correo 
                FROM usuario WHERE (cedula) = (?)
                """,
                (cedula,),
            )
            email = cursor.fetchone()
            return email
        except sqlite3.Error as e:
            print(f"Error getting details: {e}")
            return None
        finally:
            connection.close()
def geUserName(cedula):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT primerNombre, primerApellido 
                FROM usuario WHERE (cedula) = (?)
                """,
                (cedula,),
            )
            email = cursor.fetchone()
            return email
        except sqlite3.Error as e:
            print(f"Error getting details: {e}")
            return None
        finally:
            connection.close()
            
def getAllUsers():
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT cedula, primerNombre, primerApellido, correo 
                FROM usuario
                """,
            )
            email = cursor.fetchall()
            return email
        except sqlite3.Error as e:
            print(f"Error getting users: {e}")
            return None
        finally:
            connection.close()
# app/database/auth/get.py
def getProductsByProvider(rifProveedor):
    """Obtiene todos los productos de un proveedor específico"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT codigo, nombre, descripcion, stock, stockMinimo, precioUnitario
                FROM producto 
                WHERE rifProveedor = ?
                ORDER BY nombre
                """,
                (rifProveedor,),
            )
            products = cursor.fetchall()
            return products
        except sqlite3.Error as e:
            print(f"Error getting products by provider: {e}")
            return []
        finally:
            connection.close()
    return []
# En app/database/auth/get.py
def getProviderData(rif):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT nombreEmpresa, direccionEmpresa, telefono, correo
                FROM proveedor WHERE (rif) = (?)
                """,
                (rif,),
            )
            provider = cursor.fetchone()
            
            if provider:
                # Formatear teléfono para asegurar que empiece con 0
                nombre, direccion, telefono, correo = provider
                telefono_str = str(telefono)
                
                # Asegurar que el teléfono tenga 11 dígitos y empiece con 0
                if telefono_str.isdigit():
                    if len(telefono_str) == 11:
                        if not telefono_str.startswith('0'):
                            telefono_str = '0' + telefono_str[1:]
                    elif len(telefono_str) == 10:
                        telefono_str = '0' + telefono_str
                    elif len(telefono_str) < 10:
                        telefono_str = '0' + telefono_str.zfill(10)
                
                return (nombre, direccion, telefono_str, correo)
            return None
            
        except sqlite3.Error as e:
            print(f"Error getting details: {e}")
            return None
        finally:
            connection.close()
            
def getProviderProducts(rif):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT codigo, nombre ,stock, precioUnitario, descuentoDesde, descuento, stockMinimo FROM producto WHERE (rifProveedor) = (?);",(rif,))
            products = cursor.fetchall()
            return products
        except sqlite3.Error as e:
            print(f"Error getting details: {e}")
            return None
        finally:
            connection.close()
       
def getProduct(id):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT p.codigo, p.nombre, pr.nombreEmpresa, p.stock, p.precioUnitario, p.rifProveedor, p.descuento, p.descuentoDesde FROM producto p JOIN proveedor pr ON p.rifProveedor = pr.rif WHERE p.codigo = ?", (id,))
            product = cursor.fetchone()
            return product
        except sqlite3.Error as e:
            print(f"Error getting product details: {e}")
            return None
        finally:
            connection.close()
            
def getInventoryProduct(id):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM productosInventario WHERE (codigoProducto) = (?);", (id,))
            product = cursor.fetchone()
            return product
        except sqlite3.Error as e:
            print(f"Error getting product details: {e}")
            return None
        finally:
            connection.close()

def getLiteralInventoryProduct(id):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM productosInventario WHERE (codigo) = (?);", (id,))
            product = cursor.fetchone()
            return product
        except sqlite3.Error as e:
            print(f"Error getting product details: {e}")
            return None
        finally:
            connection.close()
 
def getInventoryProductQuantity(id):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT cantidad FROM productosInventario WHERE (codigoProducto) = (?);", (id,))
            product = cursor.fetchone()
            return product
        except sqlite3.Error as e:
            print(f"Error getting product details: {e}")
            return None
        finally:
            connection.close()
            
def getInventoryProducts():
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT i.codigo, pr.nombre, prov.nombreEmpresa, i.cantidad, pr.stockMinimo FROM productosInventario i JOIN producto pr ON i.codigoProducto = pr.codigo JOIN proveedor prov ON pr.rifProveedor = prov.rif;")
            products = cursor.fetchall()
            return products
        except sqlite3.Error as e:
            print(f"Error getting product details: {e}")
            return None
        finally:
            connection.close()           

def getAllCompras():
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT idCompra, nombreUsuario, fechaCompra, totalCompra FROM compra WHERE estado = 'Recibido' ORDER BY fechaCompra DESC;")
            data = cursor.fetchall()
            return data 
        except sqlite3.Error as e:
            print(f"Error getting product details: {e}")
            return None
        finally:
            connection.close()
            
def getAllSpecificCompras(code):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT 
                    dc.idCompra,
                    dc.codigoProducto,
                    dc.cantidad,
                    dc.precioUnitario,
                    dc.subTotal,
                    dc.tasaBCV  -- Agregar tasa BCV
                FROM detalleCompra dc
                JOIN compra c ON dc.idCompra = c.idCompra
                WHERE dc.idCompra = ?
                """,
                (code,)
            )
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Error getting purchase details: {e}")
            return []
        finally:
            connection.close()
    return []

            
def getLastCompra():
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(idCompra) FROM compra")
            
            result = cursor.fetchone()
            
            if result and result[0] is not None:
                return result[0]
            else:
                return 0
                
        except sqlite3.Error as e:
            print(f"Error gettin Id: {e}")
            return None
        finally:
            connection.close()