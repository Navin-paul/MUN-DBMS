import mysql.connector

print("Testing MySQL connection...")
try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Hail$hydra9",
        port=3306,
        connection_timeout=10
    )
    print("✅ Connected to MySQL.")
    conn.close()
except Exception as e:
    print("❌ Could not connect to MySQL:", e)