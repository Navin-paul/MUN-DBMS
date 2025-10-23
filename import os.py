import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

print("🔥 Starting the MUN-DBMS Data Importer...")

load_dotenv()

DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASS = 'Hail$hydra9'
DB_NAME = 'temp_db'

base_dir = os.path.dirname(os.path.abspath(__file__))
CSV_FOLDER = os.path.join(base_dir, "data_csv")
sql_file = os.path.join(base_dir, 'create_table.sql')

print(f"🔎 Looking for CSV folder at: {CSV_FOLDER}")
if not os.path.exists(CSV_FOLDER):
    print("❌ CSV folder not found! Exiting.")
    exit()
else:
    print("✅ CSV folder found.")

print(f"🔎 Looking for SQL file at: {sql_file}")
if not os.path.exists(sql_file):
    print("❌ SQL file not found! Exiting.")
    exit()
else:
    print("✅ SQL file found.")

# Connect to MySQL
print("🔌 Connecting to MySQL...")
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        port=int(os.getenv("DB_PORT", 3306)),
        connection_timeout=10  # Add a timeout to force an error if it can't connect
    )
    print("✅ Connected to MySQL.")
except Exception as e:
    print("❌ Could not connect to MySQL:", e)
    exit()

cursor = conn.cursor()

# Create database and use it
print(f"🛠️  Creating/Using database: {DB_NAME}")
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
cursor.execute(f"USE {DB_NAME}")

# Run SQL file to create tables
print("🛠️  Creating tables from SQL file...")
with open(sql_file, "r") as f:
    sql_commands = f.read().split(';')
    for command in sql_commands:
        if command.strip():
            cursor.execute(command)
print("✅ Tables created.")

# Import each CSV into its own table
print("🚀 Starting CSV import...")
for csv_file in os.listdir(CSV_FOLDER):
    if csv_file.endswith('.csv'):
        table_name = csv_file.replace(".csv", "").upper()
        file_path = os.path.join(CSV_FOLDER, csv_file)
        print(f"📂 Reading {csv_file} for table {table_name}...")
        df = pd.read_csv(file_path, delimiter=';')
        print(f"📊 Importing {len(df)} records into table {table_name}...")
        placeholders = ", ".join(["%s"] * len(df.columns))
        columns = ", ".join([f"`{col}`" for col in df.columns])
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        for _, row in df.iterrows():
            cursor.execute(insert_sql, tuple(row))
        print(f"✅ Imported {len(df)} records into {table_name}!")

conn.commit()
cursor.close()
conn.close()
print("🎉 All data imported successfully! Mission accomplished. 🚀")