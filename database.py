import sqlite3
import pandas as pd

# Database file path
DB_FILE = "healthnav.db"
CSV_FILE = "cleaned_dataset.csv"  # Ensure this CSV is in the same directory

def create_database():
    """Creates the SQLite database and required tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            insurance TEXT,
            street TEXT,
            city TEXT,
            state TEXT,
            zip TEXT
        )
    ''')

    # Create Doctors Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT,
            first_name TEXT,
            degree TEXT,
            street_address_1 TEXT,
            street_address_2 TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            country TEXT,
            phone TEXT,
            gender TEXT
        )
    ''')

    conn.commit()
    conn.close()

def load_doctors_data():
    """Loads data from `cleaned_dataset.csv` into the doctors table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Read CSV file
    df = pd.read_csv(CSV_FILE, dtype={"zip_code": str}, low_memory=False)


    # Ensure column names match the database schema
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    # Convert zip codes and phone numbers to strings (avoid scientific notation issues)
    df['zip_code'] = df['zip_code'].astype(str)
    df['phone'] = df['phone'].astype(str)

    # Insert into SQLite table
    df.to_sql("doctors", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()  # Step 1: Create tables
    load_doctors_data()  # Step 2: Load doctor data from CSV
    print("Database initialized successfully.")
