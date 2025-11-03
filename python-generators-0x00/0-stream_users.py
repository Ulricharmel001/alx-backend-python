#!/usr/bin/python3
from config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database="ALX_prodev"
    )
    return connection

def stream_users():
    """
    Generator function to stream rows from the user_data table one by one.
    Each row is returned as a dictionary.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)  # return rows as dicts
    cursor.execute("SELECT * FROM user_data;")
    
    for row in cursor:  
        yield row
    
    cursor.close()
    connection.close()
