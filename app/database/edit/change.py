import sqlite3
from app.database.connect import connectDB

def changePassword(cedula, newPassword):
    connection = connectDB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE usuario SET contrasena = ? WHERE cedula = ?", (newPassword, cedula))
            connection.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error Changing Password: {e}")
            return False
        
        finally:
            connection.close()
    return False
