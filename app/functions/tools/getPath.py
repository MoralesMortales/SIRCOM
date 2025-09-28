import sys
from pathlib import Path

def get_base_path():
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parent
    else:
        base_path = Path(__file__).parent.parent.parent
    
    return base_path

def get_db_path():
    base_path = get_base_path()
    
    if getattr(sys, 'frozen', False):
        db_path = base_path / "database.db"
    else:
        db_path = base_path / "database" / "database.db"
    
    return db_path


