import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="updproj"
)
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

