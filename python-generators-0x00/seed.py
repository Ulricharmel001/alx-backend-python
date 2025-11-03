#!/usr/bin/python3
import csv
import uuid
import mysql.connector

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_PORT
import data.csv

csv_file = data.csv

def connect_db():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()
    connection.commit()


def connect_to_prodev():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database="ALX_prodev",
            port=DB_PORT
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to ALX_prodev DB: {e}")
        return None


def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        );
        """
    )
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")


def insert_data(connection, csv_file):
    cursor = connection.cursor()

    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            name, email, age = row
            uid = str(uuid.uuid4())

            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (uid, name, email, age))

    connection.commit()
    cursor.close()
