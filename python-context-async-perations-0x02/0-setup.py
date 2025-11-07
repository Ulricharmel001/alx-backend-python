import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
""")

# insert sample rows
cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 22)")
cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 35)")
cursor.execute("INSERT INTO users (name, age) VALUES ('Charlie', 45)")

conn.commit()
conn.close()

print("database setup complete!")
