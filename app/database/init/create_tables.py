import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent.parent.parent / ".env"

load_dotenv(env_path)

HOST = os.getenv("HOST")
USERNAME = os.getenv("USERNAME")
DATABASE = os.getenv("DATABASE")
PASSWORD = os.getenv("PASSWORD")
CHARSET = os.getenv("CHARSET")


def create_tables():
    connection = pymysql.connect(
        host=HOST,
        user=USERNAME,
        database=DATABASE,
        password=PASSWORD,
        charset=CHARSET,
    )
    connection_cursor = connection.cursor()

    sql_statements = [
        """CREATE TABLE `productos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nombre` varchar(255) DEFAULT NULL,
      `descripcion` text DEFAULT NULL,
      `stock` int(11) DEFAULT NULL,
      PRIMARY KEY (`id`)
    );""",
        """CREATE TABLE `proveedores` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nombre` varchar(255) DEFAULT NULL,
      PRIMARY KEY (`id`)
    );""",
        """CREATE TABLE `entradas` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `producto_id` int(11) DEFAULT NULL,
      `cantidad` int(11) DEFAULT NULL,
      `proveedor` varchar(255) DEFAULT NULL,
      `fecha` date DEFAULT NULL,
      PRIMARY KEY (`id`),
      KEY `producto_id` (`producto_id`),
      CONSTRAINT `entradas_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
    );""",
        """CREATE TABLE `salidas` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `producto_id` int(11) DEFAULT NULL,
      `cantidad` int(11) DEFAULT NULL,
      `cliente` varchar(255) DEFAULT NULL,
      `fecha` date DEFAULT NULL,
      PRIMARY KEY (`id`),
      KEY `producto_id` (`producto_id`),
      CONSTRAINT `salidas_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
    );""",
    ]

    for statement in sql_statements:
        connection_cursor.execute(statement)

    print("Las tablas y datos han sido creados correctamente.")
    connection.commit()
