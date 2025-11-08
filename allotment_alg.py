import mysql.connector
import traceback

def connect_to_db():
    try:
        print("🔌 Attempting DB connection to localhost:3306 (user=root)")
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",  # Using the existing password from your configuration
            database="mun_management",
            connection_timeout=10,
            use_pure=True
        )
        print("✅ DB connection established")
        # Alter tables to fix Status column length
        cursor = connection.cursor()
        tables = ['aippm', 'crisis', 'unga', 'unhrc']
        for table in tables:
            try:
                print(f"🔧 Altering table `{table}`: MODIFY Status VARCHAR(20)")
                cursor.execute(f"ALTER TABLE {table} MODIFY Status VARCHAR(20)")
                connection.commit()
                print(f"✅ Modified Status column in {table}")
            except mysql.connector.Error as err:
                print(f"⚠ Error modifying {table}: {err}")
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Error connecting to database: {err}")
        print(traceback.format_exc())
        return None

def sort_delegates():
    print("▶ Starting sort_delegates()")
    connection = connect_to_db()
    if not connection:
        print("❌ Aborting sort_delegates: no DB connection")
        return

    cursor = connection.cursor()
    
    # Get all delegates sorted by points (highest to lowest) and ID (lowest to highest)
    try:
        print("📥 Querying delegates_sorted for ordering...")
        cursor.execute("""
            SELECT ID, Name, Committee, Portfolio1, Portfolio2, Points 
            FROM delegates_sorted 
            ORDER BY Points DESC, ID ASC
        """)
        delegates = cursor.fetchall()
        print(f"✅ Fetched {len(delegates)} delegates from delegates_sorted")
    except mysql.connector.Error as err:
        print(f"❌ Error fetching delegates_sorted: {err}")
        print(traceback.format_exc())
        cursor.close()
        connection.close()
        return

    # Process each delegate
    for idx, delegate in enumerate(delegates, start=1):
        delegate_id, name, committee, portfolio1, portfolio2, points = delegate
        print(f"[{idx}/{len(delegates)}] Processing delegate ID={delegate_id} Name='{name}' Committee='{committee}' Points={points}")
        print(f"    Preferences: 1='{portfolio1}' 2='{portfolio2}'")
        
        # Check Portfolio1 first
        assigned = False
        try:
            if try_assign_portfolio(cursor, committee, portfolio1, name):
                print(f"    ✅ Successfully assigned {name} to {portfolio1}")
                assigned = True
        except Exception as e:
            print(f"    ⚠ Error while trying Portfolio1 for {name}: {e}")
            print(traceback.format_exc())
            
        if assigned:
            continue
            
        # If Portfolio1 is not available, try Portfolio2
        try:
            if try_assign_portfolio(cursor, committee, portfolio2, name):
                print(f"    ✅ Successfully assigned {name} to {portfolio2}")
                assigned = True
        except Exception as e:
            print(f"    ⚠ Error while trying Portfolio2 for {name}: {e}")
            print(traceback.format_exc())
            assigned = False
        
        if not assigned:
            print(f"    ⚠ Could not assign {name} to any portfolio")

    try:
        connection.commit()
        print("💾 All changes committed to DB")
    except Exception as e:
        print("⚠ Error during commit:", e)
        print(traceback.format_exc())
    finally:
        cursor.close()
        connection.close()
        print("🔒 DB connection closed")

def try_assign_portfolio(cursor, committee, portfolio, delegate_name):
    # Skip if any parameter is None
    if not all([committee, portfolio, delegate_name]):
        print(f"    ℹ Skipping assignment due to missing data - Committee: {committee}, Portfolio: {portfolio}, Name: {delegate_name}")
        return False

    # Map committee names to table names
    committee_tables = {
        'AIPPM': 'aippm',
        'CRISIS': 'crisis',
        'UNGA': 'unga',
        'UNHRC': 'unhrc'
    }
    
    table_name = committee_tables.get(committee)
    if not table_name:
        print(f"    ⚠ Committee '{committee}' not found in mapping")
        return False

    try:
        # Check if the portfolio exists and is available in the committee
        query = f"""
            SELECT ID, Portfolio, Status
            FROM {table_name} 
            WHERE Portfolio = %s 
            AND Status = 'Available'
        """
        print(f"    🔎 Checking `{table_name}` for portfolio='{portfolio}' availability")
        cursor.execute(query, (portfolio,))
        
        result = cursor.fetchone()
        if result:
            print(f"    ➤ Found available portfolio in `{table_name}`: {result}")
            # Update the portfolio assignment
            update_sql = f"""
                UPDATE {table_name} 
                SET Status = 'Unavailable', Delegate = %s 
                WHERE Portfolio = %s AND Status = 'Available'
            """
            print(f"    🔁 Updating `{table_name}` set Delegate='{delegate_name}', Status='Unavailable' for Portfolio='{portfolio}'")
            cursor.execute(update_sql, (delegate_name, portfolio))
            return True
        else:
            print(f"    ➤ Portfolio '{portfolio}' not available in `{table_name}`")
            
    except mysql.connector.Error as err:
        print(f"    ❌ Error assigning portfolio in {table_name}: {err}")
        print(traceback.format_exc())
        
    return False

def check_crisis_table():
    print("▶ Running check_crisis_table()")
    connection = connect_to_db()
    if not connection:
        print("❌ Aborting check_crisis_table: no DB connection")
        return

    cursor = connection.cursor()
    print("\nChecking Crisis delegates and assignments:")
    
    # First check all possible variations of Crisis committee name
    try:
        print("📥 Querying delegates_sorted WHERE Committee = 'CRISIS'")
        cursor.execute("""
            SELECT ID, Name, Committee, Portfolio1, Portfolio2, Points 
            FROM delegates_sorted 
            WHERE Committee = 'CRISIS'
            ORDER BY Points DESC
        """)
        crisis_delegates = cursor.fetchall()
    except mysql.connector.Error as err:
        print("❌ Error querying delegates_sorted for CRISIS:", err)
        crisis_delegates = []
    
    if not crisis_delegates:
        print("   ℹ No delegates found requesting Crisis committee")
    else:
        print(f"   ✅ Found {len(crisis_delegates)} delegates requesting Crisis committee:")
        for row in crisis_delegates:
            print(f"      ID: {row[0]}, Name: {row[1]}, Committee: {row[2]}, Points: {row[5]}, Portfolio1: {row[3]}, Portfolio2: {row[4]}")
    
    # Check Crisis portfolios
    try:
        print("\n📥 Querying all rows from `crisis` table")
        cursor.execute("SELECT * FROM crisis")
        portfolios = cursor.fetchall()
    except mysql.connector.Error as err:
        print("❌ Error querying crisis table:", err)
        portfolios = []
    if not portfolios:
        print("   ℹ No portfolios found in crisis table")
    else:
        print(f"   ✅ Found {len(portfolios)} portfolios in crisis table:")
        for row in portfolios:
            print(f"      ID: {row[0]}, Portfolio: {row[1]}, Status: {row[2]}, Delegate: {row[3]}")
    
    cursor.close()
    connection.close()
    print("🔒 check_crisis_table finished and DB connection closed")

if __name__ == "__main__":
    try:
        sort_delegates()
        check_crisis_table()
        print("🎉 Done.")
    except Exception as e:
        print("❌ Unexpected error in main:", e)
        print(traceback.format_exc())
