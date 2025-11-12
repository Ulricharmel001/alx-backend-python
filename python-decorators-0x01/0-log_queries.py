import sqlite3
import functools

#### decorator to lof SQL queries

class log_queries:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        query = kwargs.get('query', '') if 'query' in kwargs else args[1] if len(args) > 1 else ''
        print(f"[LOG] Executing query: {query}")
        return self.func(*args, **kwargs)
    def __get__(self, instance, owner):
        return functools.partial(self.__call__, instance)
#### usage example

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")