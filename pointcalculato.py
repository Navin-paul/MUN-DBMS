import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="updproj"
)
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS delegates_points")

# Create new table with Points column
cur.execute("""
CREATE TABLE delegates_points AS
SELECT *, 0 AS Points
FROM delegates
""")

# Points system
points_map = {"BD": 9, "HC": 5, "SM": 3, "HM": 2, "VM": 1, "MUNs": 1}

# Fetch all records from the new table
cur.execute("SELECT * FROM delegates_points")
rows = cur.fetchall()

# Calculate points and update
for row in rows:
    points = (row[8]*points_map["BD"]+row[9]*points_map["HC"]+row[10]*points_map["SM"] + row[11]*points_map["HM"] +
              row[12]*points_map["VM"] + row[4]*points_map["MUNs"])
    cur.execute("UPDATE delegates_points SET Points=%s WHERE Name=%s", (points, row[1]))

conn.commit()

# Generate INSERT statements for another table
for record in cur.fetchall():
    values = []
    for val in record:
        if isinstance(val, str):
                values.append("'" + val.replace("'", "''") + "'")  # escape single quote
        else:
            values.append(str(val))
    insert_stmt = f"INSERT INTO sorted_delegates VALUES ({', '.join(values)});"
    print(insert_stmt)

cur.close()
conn.close()