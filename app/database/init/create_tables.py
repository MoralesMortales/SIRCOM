import os
import sqlite3

DB_PATH = os.getenv("DB_PATH", "app/database/database.db")


def create_tables():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection_cursor = connection.cursor()

        sql_statements = [
            """CREATE TABLE IF NOT EXISTS productos (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          nombre TEXT,
          descripcion TEXT,
          stock INTEGER
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
            connection.close()
