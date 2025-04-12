import sqlite3
import pandas as pd
import os


# Database file path
DB_FILE = "healthnav.db"
CSV_FILE = "MI_Doctors.csv"  # Ensure this CSV is in the same directory

def create_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
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
            row_id INTEGER,
            npi TEXT,
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
            gender TEXT,
            specialty TEXT
        )
    ''')

    conn.commit()
    conn.close()

def load_doctors_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    df = pd.read_csv(CSV_FILE, dtype={"zip_code": str}, low_memory=False)
    df.rename(columns={"Unnamed: 0": "row_id", "NPI": "npi"}, inplace=True)

    df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    df['zip_code'] = df['zip_code'].astype(str)
    df['phone'] = df['phone'].astype(str)

    df.to_sql("doctors", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    load_doctors_data()
    print("Database initialized successfully.")