import sqlite3

def get_mock_db_connection():
    # Creates a temporary database entirely in RAM that deletes itself when the app closes
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    # Create mock tables to simulate a real production database schema
    cursor.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,
            total_amount REAL,
            status TEXT
        )
    """)
    
    # Create an index on customer_id to show the difference between indexed seeks and unindexed scans
    cursor.execute("CREATE INDEX idx_orders_customer ON orders(customer_id)")
    
    conn.commit()
    return conn

def run_explain_plan(query):
    conn = get_mock_db_connection()
    cursor = conn.cursor()
    try:
        # Inject the EXPLAIN QUERY PLAN command directly in front of the user's SQL
        explain_query = f"EXPLAIN QUERY PLAN {query}"
        cursor.execute(explain_query)
        plan_rows = cursor.fetchall()
        
        # Format the output into clean text lines
        # plan_rows structure: (id, parent, notused, detail_text)
        plan_details = [row[3] for row in plan_rows]
        return plan_details, None
    except sqlite3.Error as e:
        # Catch real syntax or table name errors
        return [], str(e)
    finally:
        conn.close()
        