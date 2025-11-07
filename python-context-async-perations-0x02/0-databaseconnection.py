import sqlite3
class DatabaseConnection:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor      # we return cursor because we want to use it inside with

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


if __name__ == "__main__":
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        print(rows)
        