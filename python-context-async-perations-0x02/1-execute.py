import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_path="mydatabase.db"):
        self.query = query
        self.params = params or []
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        # do not suppress exception
        return False


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    with ExecuteQuery(query, param) as result:
        print(result)
