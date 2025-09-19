import os
import sys
from pathlib import Path
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))

import sqlite3
from app.database.connect import connectDB
from app.database.init.create_tables import create_tables

DB_PATH = os.getenv("DB_PATH", "app/database/database.db")

def database_exist():

    connection = None

    try:
        db_file = Path(DB_PATH)
        
        if not db_file.exists():
            print(f"La base de datos '{DB_PATH}' no existe. Creándola...")
            connection = connectDB()
            connection.close()
            
            print(f"La base de datos ha sido creada exitosamente.")
            
            create_tables()
            
        else:
            print(f"La base de datos ya existe.")
            
            connection = connectDB()
            cursor = connection.cursor()
            
            cursor.execute("SELECT * FROM sqlite_master ")
            if not cursor.fetchone():
                print( cursor.fetchone())
                print("Las tablas no existen. Creándolas...")
                create_tables()
            else:
                print("Las tablas ya existen.")
                
            connection.close()

    except sqlite3.Error as e:
        print(f"Error al configurar la base de datos: {e}")

    except Exception as e:
        print(f"Error inesperado: {e}")

    finally:
        if connection:
            connection.close()
