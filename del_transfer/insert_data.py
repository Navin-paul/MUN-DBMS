import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import sys

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASSWORD", "")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "mun_management") 

base_dir = os.path.dirname(os.path.abspath(__file__))
CSV_FOLDER = os.path.join(base_dir, "data_csv")
SQL_FILE = os.path.join(base_dir, "create_table.sql")

print("🔥 Starting the MUN-DBMS Data Importer...")
print(f"🔎 Looking for CSV folder at: {CSV_FOLDER}")
if not os.path.isdir(CSV_FOLDER):
    print("❌ CSV folder not found. Exiting.")
    sys.exit(1)
print("✅ CSV folder found.")

print(f"🔎 Looking for SQL file at: {SQL_FILE}")
if not os.path.isfile(SQL_FILE):
    print("❌ SQL file not found. Exiting.")
    sys.exit(1)
print("✅ SQL file found.")

# Connect to MySQL with timeout and error reporting
print("🔌 Connecting to MySQL...")
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        connection_timeout=10,
        use_pure=True
    )
    print("✅ Connected to MySQL.")
except Exception as e:
    print("❌ Could not connect to MySQL:", e)
    sys.exit(1)

cursor = conn.cursor()

# Create database if not exists and switch to it
try:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
    cursor.execute(f"USE `{DB_NAME}`")
    print(f"🛠 Using database: {DB_NAME}")
except Exception as e:
    print("❌ Database creation/use failed:", e)
    conn.close()
    sys.exit(1)

# Execute SQL file (creates tables)
print("🛠 Running SQL file to create tables...")
with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql_text = f.read()
for stmt in sql_text.split(';'):
    stmt = stmt.strip()
    if not stmt:
        continue
    try:
        cursor.execute(stmt)
    except Exception as e:
        print("⚠ Error executing SQL statement (continuing):", e)

# Get CSV files
csv_files = [f for f in os.listdir(CSV_FOLDER) if f.lower().endswith(".csv")]
if not csv_files:
    print("❌ No CSV files found. Exiting.")
    cursor.close()
    conn.close()
    sys.exit(1)

# Import each CSV into its own table
for csv_file in csv_files:
    csv_path = os.path.join(CSV_FOLDER, csv_file)
    table_name = os.path.splitext(csv_file)[0]  # adjust case if needed
    # If your SQL uses uppercase table names uncomment next line:
    # table_name = table_name.upper()

    print(f"📂 Reading {csv_file} -> target table `{table_name}`")
    try:
        df = pd.read_csv(csv_path, delimiter=';', dtype=object)  # read as strings to avoid dtype issues
    except Exception as e:
        print(f"❌ Failed to read {csv_file}:", e)
        continue

    if df.empty:
        print(f"⚠ {csv_file} is empty — skipping.")
        continue

    # Normalize column names to match SQL if needed (comment/uncomment as required)
    cols = list(df.columns)
    columns_sql = ", ".join([f"`{c}`" for c in cols])
    placeholders = ", ".join(["%s"] * len(cols))
    insert_sql = f"INSERT INTO `{table_name}` ({columns_sql}) VALUES ({placeholders})"

    inserted = 0
    for _, row in df.iterrows():
        values = [None if pd.isna(row[c]) else row[c] for c in cols]
        try:
            cursor.execute(insert_sql, tuple(values))
            inserted += 1
        except Exception as e:
            print(f"   ⚠ Row insert error into `{table_name}`: {e} -- skipping row")

    conn.commit()
    print(f"✅ Imported {inserted}/{len(df)} rows into `{table_name}`")

# Cleanup
cursor.close()
conn.close()
print("🎉 All done. Data import finished.")
