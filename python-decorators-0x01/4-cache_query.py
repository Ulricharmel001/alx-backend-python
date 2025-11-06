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


query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("[CACHE] Returning cached result")
            return query_cache[query]
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# Combine with connection decorator
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call caches the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call uses cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
