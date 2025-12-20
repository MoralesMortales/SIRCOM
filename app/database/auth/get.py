from pathlib import Path
import sys

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))

import sqlite3

from app.database.connect import connectDB

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
            return provider
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
            cursor.execute("SELECT codigo, nombre ,stock, precioUnitario FROM producto WHERE (rifProveedor) = (?);",(rif,))
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
            cursor.execute("SELECT p.codigo, p.nombre, pr.nombreEmpresa, p.stock, p.precioUnitario FROM producto p JOIN proveedor pr ON p.rifProveedor = pr.rif WHERE p.codigo = ?", (id,))
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
            cursor.execute("SELECT i.codigo, pr.nombre, prov.nombreEmpresa, i.cantidad FROM productosInventario i JOIN producto pr ON i.codigoProducto = pr.codigo JOIN proveedor prov ON pr.rifProveedor = prov.rif;")
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
            cursor.execute("SELECT idCompra, nombreUsuario, fechaCompra, totalCompra FROM compra;")
            data = cursor.fetchall()
            return data
        except sqlite3.Error as e:
            print(f"Error getting product details: {e}")
            return None
        finally:
            connection.close()
            
def getAllSpecificCompras(codigo):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT idCompra, codigoProducto, cantidad, precioUnitario, subTotal FROM detalleCompra WHERE (idCompra) = (?);", (codigo,))
            data = cursor.fetchall()
            return data
        except sqlite3.Error as e:
            print(f"Error getting product details: {e}")
            return None
        finally:
            connection.close()

            
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