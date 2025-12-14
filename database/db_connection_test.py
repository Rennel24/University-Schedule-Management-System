import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  

try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")

    print("Connected successfully!\nTables in database:")
    for (table,) in cursor.fetchall():
        print("-", table)

    conn.close()

except mysql.connector.Error as e:
    print("Database connection failed!")
    print("Error:", e)
