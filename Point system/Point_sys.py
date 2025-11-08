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

# recreate delegates_points from delegates
try:
    cur.execute("DROP TABLE IF EXISTS delegates_points")
    cur.execute("""
        CREATE TABLE delegates_points AS
        SELECT *, 0 AS Points
        FROM delegates
    """)
    conn.commit()
except Exception as e:
    print("⚠ Error creating delegates_points:", e)

# points mapping
points_map = {"BD": 9, "HC": 5, "SM": 3, "HM": 2, "VM": 1, "MUNs": 1}

# select needed columns (use column names to avoid index errors)
cur.execute("SELECT ID, Name, BD, HC, SM, HM, VM, MUNs FROM delegates_points")
rows = cur.fetchall()

# update Points using ID for WHERE
for row in rows:
    id_, name, bd, hc, sm, hm, vm, muns = row
    # convert None to 0 and to int where possible
    def to_int(x):
        try:
            return int(x) if x is not None else 0
        except:
            return 0
    score = (
        to_int(bd) * points_map["BD"] +
        to_int(hc) * points_map["HC"] +
        to_int(sm) * points_map["SM"] +
        to_int(hm) * points_map["HM"] +
        to_int(vm) * points_map["VM"] +
        to_int(muns) * points_map["MUNs"]
    )
    try:
        cur.execute("UPDATE delegates_points SET Points=%s WHERE ID=%s", (score, id_))
    except Exception as e:
        print(f"⚠ Failed to update ID={id_} ({name}):", e)

conn.commit()
print("✅ Points calculated and updated.")

# generate INSERT statements for sorted_delegates (select from delegates_points)
try:
    cur.execute("SELECT * FROM delegates_points")
    all_rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    for record in all_rows:
        values = []
        for val in record:
            if val is None:
                values.append("NULL")
            elif isinstance(val, str):
                values.append("'" + val.replace("'", "''") + "'")
            else:
                values.append(str(val))
        insert_stmt = f"INSERT INTO sorted_delegates ({', '.join('`'+c+'`' for c in cols)}) VALUES ({', '.join(values)});"
        print(insert_stmt)
except Exception as e:
    print("⚠ Could not generate INSERT statements:", e)

cur.close()
conn.close()
print("Done.")
