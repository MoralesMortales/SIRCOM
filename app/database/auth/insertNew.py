from pathlib import Path
import sys

from app.database.auth.update import updatePurchaseStatus

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
            print(f"Integrity Error): {e}")
            return False       
        
        except sqlite3.Error as e:
            print(f"Error inserting new user: {e}")
            return False
        
        finally:
            connection.close()

def newProduct(nombre, precioUnitario, stock, RIF,min_desc=0, descuento=0, stock_min=0, description="", codigo=None):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
INSERT INTO producto (codigo, nombre, precioUnitario, stock, rifProveedor, descuentoDesde, descuento, stockMinimo, descripcion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)                """,
                (codigo,nombre, precioUnitario,stock, RIF, min_desc, descuento, stock_min, description),
            )
            connection.commit()
            return True
        
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error): {e}")
            return False       
        
        except sqlite3.Error as e:
            print(f"Error inserting new product: {e}")
            return False
        
        finally:
            connection.close()
            
def newProvider(RIF, nombreEmpresa, DireccionEmpresa, telefono, correo):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                insert into proveedor (rif, nombreEmpresa,DireccionEmpresa,telefono,correo) VALUES (?,?,?,?,?)
                """,
                (RIF, nombreEmpresa,DireccionEmpresa, telefono, correo),
            )
            connection.commit()
            return True
        
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error): {e}")
            return False       
        
        except sqlite3.Error as e:
            print(f"Error inserting new provider: {e}")
            return False
        
        finally:
            connection.close()
            

def newInventoryProduct(codigoProducto, cantidad):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                insert into productosInventario (codigoProducto, cantidad, stock_minimo) VALUES (?,?,?)
                """,
                (codigoProducto, cantidad, 0),
            )
            connection.commit()
            return True
        
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error): {e}")
            return False       
        
        except sqlite3.Error as e:
            print(f"Error inserting new product in inventory: {e}")
            return False
        
        finally:
            connection.close()
            
def newcompra(totalCompra, nombreUsuario, estado="En Curso"):
    """Crea una nueva compra con estado inicial"""
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO compra (totalCompra, nombreUsuario, estado) VALUES (?, ?, ?)",
                (totalCompra, nombreUsuario, estado)
            )
            connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating new purchase: {e}")
            return None
        finally:
            connection.close()
    return None

def updatePurchaseOrder(purchase_id, status):
    """Actualiza el estado de una orden de compra (alias para updatePurchaseStatus)"""
    return updatePurchaseStatus(purchase_id, status)

         
def newDetailCompra(idCompra, codigoProducto, cantidad, precioUnitario, subTotal, tasa):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                insert into detalleCompra (idCompra, codigoProducto, cantidad, precioUnitario, subTotal, tasaBCV) VALUES (?,?,?,?,?,?)
                """,
                (idCompra, codigoProducto, cantidad, precioUnitario, subTotal, tasa),
            )
            connection.commit()
            return True
        
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error): {e}")
            return False       
        
        except sqlite3.Error as e:
            print(f"Error inserting new product in inventory: {e}")
            return False
        
        finally:
            connection.close()