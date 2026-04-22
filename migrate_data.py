import sqlite3
import pandas as pd
from utils.sheets_utils import get_spreadsheet

def migrate_sqlite_to_sheets():
    """Migrate data from SQLite database to Google Sheets"""

    # Connect to SQLite
    sqlite_conn = sqlite3.connect('hiv.db')

    # Get Google Sheets spreadsheet
    sheet = get_spreadsheet()

    # Migration mapping
    migrations = {
        'patients': 'Patients',
        'hiv_testing': 'HIV_Testing',
        'treatment': 'Treatment',
        'facilities': 'Facilities'
    }

    for sqlite_table, sheet_name in migrations.items():
        print(f"Migrating {sqlite_table} to {sheet_name}...")

        # Load data from SQLite
        df = pd.read_sql(f"SELECT * FROM {sqlite_table}", sqlite_conn)

        if not df.empty:
            # Get worksheet
            worksheet = sheet.worksheet(sheet_name)

            # Clear existing data (keep headers)
            worksheet.clear()

            # Convert to list of lists for gspread
            data = [df.columns.tolist()] + df.values.tolist()

            # Update worksheet
            worksheet.update(data)

            print(f"✅ Migrated {len(df)} records to {sheet_name}")
        else:
            print(f"⚠️  No data in {sqlite_table}")

    sqlite_conn.close()
    print("\n🎉 Migration complete!")

if __name__ == "__main__":
    migrate_sqlite_to_sheets()