# MUN Delegate Database

This repository creates and fills a MySQL database with delegate data.

## Setup

1. Clone this repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Edit `env` with your MySQL credentials.
4. Run:
   ```bash
   python insert_data.py
   ```

✅ The table `database be created and filled automaticaly


this is how the final output here must look like 
|
|

(.venv) PS C:\Users\NeethuPaul\Documents\GitHub\MUN-DBMS> & C:/Users/NeethuPaul/Documents/GitHub/MUN-DBMS/.venv/Scripts/python.exe c:/Users/NeethuPaul/Documents/GitHub/MUN-DBMS/del_transfer/insert_data.py
🔥 Starting the MUN-DBMS Data Importer...
🔎 Looking for CSV folder at: c:\Users\NeethuPaul\Documents\GitHub\MUN-DBMS\del_transfer\data_csv
✅ CSV folder found.
🔎 Looking for SQL file at: c:\Users\NeethuPaul\Documents\GitHub\MUN-DBMS\del_transfer\create_table.sql
✅ SQL file found.
🔌 Connecting to MySQL...
✅ Connected to MySQL.
🛠 Using database: temp_db
🛠 Running SQL file to create tables...
📂 Reading aippm.csv -> target table `aippm`
✅ Imported 41/41 rows into `aippm`
📂 Reading crisis.csv -> target table `crisis`
✅ Imported 39/39 rows into `crisis`
📂 Reading delegates.csv -> target table `delegates`
✅ Imported 180/180 rows into `delegates`
📂 Reading unga.csv -> target table `unga`
✅ Imported 39/39 rows into `unga`
📂 Reading unhrc.csv -> target table `unhrc`
✅ Imported 39/39 rows into `unhrc`
🎉 All done. Data import finished.
(.venv) PS C:\Users\NeethuPaul\Documents\GitHub\MUN-DBMS> 