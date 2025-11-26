import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="university_schedule_db"  
    )

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")

    print("Connected successfully! \nTables in database:")
    for (table,) in cursor.fetchall():
        print("-", table)

    conn.close()

except mysql.connector.Error as e:
    print("Database connection failed!")
    print("Error:", e)
