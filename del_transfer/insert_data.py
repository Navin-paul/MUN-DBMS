import pandas as pd
import mysql.connector
import os   
from dotenv import load_dotenv 

load_dotenv()

# -------------------------------

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')
DB_NAME = 'temp_db'  # Temporary DB for initial setup
base_dir = os.path.dirname(os.path.abspath(__file__))
CSV_FOLDER ="C:\Users\NeethuPaul\Documents\GitHub\MUN-DBMS\data_csv"
sql_file = os.path.join(base_dir, 'create_table.sql')

# -------------------------------
print(f"DB_HOST={DB_HOST}, DB_USER={DB_USER}, DB_PASS={DB_PASS}")


#data_folder =   # replace with your actual folder name 

print("Looking for folder:", CSV_FOLDER)
print("Exists?", os.path.exists(CSV_FOLDER))


# --- Check if SQL file exists ---
if not os.path.exists(sql_file):
    print(f"❌ SQL file not found: {sql_file}")
else:
    print(f"✅ SQL file found: {sql_file}")

  # your folder name

all_files = [f for f in os.listdir(CSV_FOLDER) if f.endswith(".csv")]
if not all_files:
    print("No CSV files found in folder:", CSV_FOLDER)
    exit()

# Read all CSVs into a single DataFrame
df_list = []
for file in all_files:
    file_path = os.path.join(CSV_FOLDER, file)
    df_list.append(pd.read_csv(file_path, delimiter=';'))

df = pd.concat(df_list, ignore_index=True)
print("All CSV files read successfully!")
print(df.head())







# Connect to MySQL
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS
)
print("🔌 Connecting to MySQL...")

cursor = conn.cursor()

# Create database if not exists
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
cursor.execute(f"USE {DB_NAME}")

# Tables creation
with open("create_table.sql", "r") as f:
    sql_commands=f.read().split(';')
    for command in sql_commands:
        if command.strip(): # No empty commands
            cursor.execute(command)

# Load CSV
for csv_file in os.listdir(CSV_FOLDER):
    if csv_file.endswith('.csv'):
        table_name = csv_file.replace(".csv", "")
        df = pd.read_csv(os.path.join(CSV_FOLDER, csv_file), delimiter=';')
        
        # Build placeholders dynamically
        placeholders = ", ".join(["%s"] * len(df.columns))
        columns = ", ".join(df.columns)
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        for _, row in df.iterrows():
            cursor.execute(insert_sql, tuple(row))

conn.commit()
conn.close()
print("✅ Data imported successfully!")
