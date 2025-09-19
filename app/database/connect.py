import os
import sqlite3
DB_PATH = os.getenv("DB_PATH", "app/database/database.db")
import sys
from pathlib import Path
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))
def connectDB():
    try:
        conection = sqlite3.connect(DB_PATH) 
        return conection
    except sqlite3.Error as e:
        print(f"Error connecting the DB: {e}")
        return None


