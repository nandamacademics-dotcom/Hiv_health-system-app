import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets configuration
SPREADSHEET_ID = "1kgbCBC0jzEsmMdyrCpw1uHtF33qhMGmwQRlSNrUau10"
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def get_google_sheets_client():
    """Get authenticated Google Sheets client"""
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPE)
    client = gspread.authorize(creds)
    return client

def get_spreadsheet():
    """Get the main spreadsheet"""
    client = get_google_sheets_client()
    try:
        return client.open_by_key(SPREADSHEET_ID)
    except gspread.SpreadsheetNotFound:
        st.error(
            "Google Sheet not found. Check that the spreadsheet ID is correct and that the service account has access."
        )
        raise
    except gspread.exceptions.APIError:
        st.error(
            "Google Sheets API error. Make sure the service account credentials in Streamlit secrets are correct and the spreadsheet is shared with the service account email."
        )
        raise

def load_worksheet_data(worksheet_name):
    """Load data from a worksheet and clean column names"""
    sheet = get_spreadsheet()
    try:
        worksheet = sheet.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        st.error(
            f"Worksheet '{worksheet_name}' was not found. Verify the tab name in your Google Sheet."
        )
        return pd.DataFrame(), None
    try:
        data = worksheet.get_all_records()
    except gspread.exceptions.APIError:
        st.error(
            f"Failed to load worksheet '{worksheet_name}'. Check spreadsheet permissions and API access."
        )
        raise
    df = pd.DataFrame(data)
    if not df.empty:
        df.columns = df.columns.str.strip()  # Remove whitespace from column names
    return df, worksheet

def get_patients_data():
    """Get patients data"""
    return load_worksheet_data("Patients")

def get_testing_data():
    """Get HIV testing data"""
    return load_worksheet_data("HIV_Testing")

def get_treatment_data():
    """Get treatment data"""
    return load_worksheet_data("Treatment")

def get_facilities_data():
    """Get facilities data"""
    return load_worksheet_data("Facilities")