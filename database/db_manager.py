import sqlite3

def init_db():
    conn = sqlite3.connect("hiv.db", check_same_thread=False)
    cursor = conn.cursor()

    # Patients
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        sex TEXT,
        age INTEGER
    )
    """)

    # HIV Testing
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hiv_testing (
        test_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        test_date TEXT,
        result TEXT
    )
    """)

    # Treatment
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treatment (
        treatment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        ART_status TEXT,
        pregnancy_status TEXT
    )
    """)

    # Facilities
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facilities (
        facility_id INTEGER PRIMARY KEY AUTOINCREMENT,
        facility_name TEXT,
        township TEXT,
        state TEXT
    )
    """)

    conn.commit()
    return conn


def get_connection():
    return sqlite3.connect("hiv.db", check_same_thread=False)