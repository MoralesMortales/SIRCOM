import os
import sqlite3

import sys
from pathlib import Path

from app.functions.tools.getPath import get_db_path

from app.database.connect import connectDB

DB_PATH = get_db_path()

def create_tables():
    try:
        connection = connectDB()
        connection_cursor = connection.cursor()

        sql_statements = [
      
          """CREATE TABLE IF NOT EXISTS proveedor (
          rif INTEGER PRIMARY KEY,
          nombreEmpresa TEXT,
          direccionEmpresa TEXT,
          telefono INTEGER,
          correo TEXT,
          estado INTEGER DEFAULT 1
        );""",

          """CREATE TABLE IF NOT EXISTS usuario (
          cedula INTEGER PRIMARY KEY,
          primerNombre TEXT,
          primerApellido TEXT,
          correo TEXT UNIQUE,
          contrasena TEXT,
          creado DATETIME DEFAULT CURRENT_TIMESTAMP
        );""",

          """CREATE TABLE IF NOT EXISTS producto (
          codigo INTEGER PRIMARY KEY AUTOINCREMENT,
          nombre TEXT,
          precioUnitario FLOAT,
          
          descuentoDesde INTEGER,
          descuento INTEGER,
          stockMinimo INTEGER,
          
          stock INTEGER,
          rifProveedor INTEGER,
          estado INTEGER DEFAULT 1,
          FOREIGN KEY (rifProveedor) REFERENCES proveedor (rif)
        );""",

            """CREATE TABLE IF NOT EXISTS compra (
          idCompra INTEGER PRIMARY KEY AUTOINCREMENT,
          fechaCompra DATETIME DEFAULT CURRENT_TIMESTAMP,
          totalCompra FLOAT,
          nombreUsuario TEXT
        );""",

          """CREATE TABLE IF NOT EXISTS detalleCompra (
          idDetalleProducto INTEGER PRIMARY KEY AUTOINCREMENT,
          idCompra INTEGER,
          codigoProducto INTEGER,
          cantidad FLOAT,
          precioUnitario FLOAT,
          subTotal FLOAT,
          FOREIGN KEY (idCompra) REFERENCES compra (idCompra),
          FOREIGN KEY (codigoProducto) REFERENCES producto (codigo)
        );""",
        
          """CREATE TABLE IF NOT EXISTS productosInventario (
          codigo INTEGER PRIMARY KEY AUTOINCREMENT,
          codigoProducto INTEGER,
          cantidad INTEGER,
          stock_minimo INTEGER,
          FOREIGN KEY (codigoProducto) REFERENCES producto (codigo)
        );""",
        
          ]

        for statement in sql_statements:
            connection_cursor.execute(statement)

        print("Las tablas y datos han sido creados correctamente.")
        connection.commit()

    except sqlite3.Error as e:
        print(f"Error al configurar la base de datos: {e}")
        if connection:
            connection.rollback()

    finally:
        if connection:
            connection.close()
