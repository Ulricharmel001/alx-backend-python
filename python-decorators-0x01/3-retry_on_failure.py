import time
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

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[WARNING] Attempt {attempt} failed: {e}")
                    if attempt == retries:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

# Combine with connection decorator
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users
users = fetch_users_with_retry()
print(users)
