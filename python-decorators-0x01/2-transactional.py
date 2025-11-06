import sqlite3
import functools
import importlib.util
import sys
from pathlib import Path

# Path to the file
file_path = Path(__file__).parent / "1-with_db_connection.py"

# Create a module spec
spec = importlib.util.spec_from_file_location("with_db_connection_module", file_path)
module = importlib.util.module_from_spec(spec)
sys.modules["with_db_connection_module"] = module
spec.loader.exec_module(module)

# Ready to use 
with_db_connection = module.with_db_connection

# Decorator to manage transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit if successful
            return result
        except Exception as e:
            conn.rollback()  # Rollback if error
            print(f"[ERROR] Transaction failed: {e}")
            raise
    return wrapper

# Combine with connection decorator
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Usage
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
