import sqlite3
from app.functions.tools.getPath import get_db_path

def connectDB():
    try:
        db_path = get_db_path()
        
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Connecting to database at: {db_path}")
        connection = sqlite3.connect(str(db_path))
        connection.execute("PRAGMA foreign_keys = ON")
        return connection
        
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise e
