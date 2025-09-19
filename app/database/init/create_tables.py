import os
import sqlite3

import sys
from pathlib import Path
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))

from app.database.connect import connectDB

DB_PATH = os.getenv("DB_PATH", "app/database/database.db")


def create_tables():
    try:
        connection = connectDB()
        connection_cursor = connection.cursor()

        sql_statements = [
            """CREATE TABLE IF NOT EXISTS productos (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          nombre TEXT,
          descripcion TEXT,
          stock INTEGER
        );""",
            """CREATE TABLE IF NOT EXISTS usuarios (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          cedula TEXT,
          clave TEXT
        );""",
            """CREATE TABLE IF NOT EXISTS proveedores (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          nombre TEXT
        );""",
            """CREATE TABLE IF NOT EXISTS clientes (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          nombre TEXT
        );""",
            """CREATE TABLE IF NOT EXISTS entradas (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          producto_id INTEGER,
          cantidad INTEGER,
          proveedor TEXT,
          fecha DATE,
          FOREIGN KEY (producto_id) REFERENCES productos (id)
        );""",
            """CREATE TABLE IF NOT EXISTS salidas (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          producto_id INTEGER,
          cantidad INTEGER,
          cliente TEXT,
          fecha DATE,
          FOREIGN KEY (producto_id) REFERENCES productos (id)
        );""",
            """INSERT INTO usuarios (cedula, clave) VALUES ("31034825", "12345678")"""
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
