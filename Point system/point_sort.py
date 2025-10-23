import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("DB_HOST", "127.0.0.1")
USER = os.getenv("DB_USER", "root")
PASSWORD = os.getenv("DB_PASSWORD", "")
PORT = int(os.getenv("DB_PORT", 3306))
DATABASE = os.getenv("DB_NAME", "mun_management")

# connect with proper keyword names and error handling
try:
    conn = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        port=PORT,
        database=DATABASE,
        connection_timeout=10,
        use_pure=True
    )
    print("✅ Connected to MySQL")
except Exception as e:
    print("❌ Connection failed:", e)
    raise SystemExit(1)

cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS delegates_sorted")
# Update table sorted by Points descending
cur.execute("""
    CREATE TABLE delegates_sorted AS
    SELECT * FROM delegates_points ORDER BY Points DESC
""")
conn.commit()
cur.close()
conn.close()
print("✅ delegates_sorted table created successfully.")

