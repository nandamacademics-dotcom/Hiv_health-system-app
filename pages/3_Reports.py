import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.title("Dashboard")

# Connect to Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("hiv-health-system-app-7ffa50f21021.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1kgbCBC0jzEsmMdyrCpw1uHtF33qhMGmwQRlSNrUau10")

# Load data from Google Sheets
testing_sheet = sheet.worksheet("HIV_Testing")
testing_data = testing_sheet.get_all_records()
testing = pd.DataFrame(testing_data)
if not testing.empty:
    testing.columns = testing.columns.str.strip()  # Remove whitespace from column names

treatment_sheet = sheet.worksheet("Treatment")
treatment_data = treatment_sheet.get_all_records()
treatment = pd.DataFrame(treatment_data)
if not treatment.empty:
    treatment.columns = treatment.columns.str.strip()  # Remove whitespace from column names

# Metrics
st.metric("Total Tested", len(testing))
if not testing.empty and "result" in testing.columns:
    st.metric("Positive Cases", len(testing[testing["result"] == "Positive"]))

if not treatment.empty and "ART_status" in treatment.columns:
    st.metric("On ART", len(treatment[treatment["ART_status"] == "On ART"]))

# Charts
if not testing.empty and "result" in testing.columns:
    st.bar_chart(testing["result"].value_counts())

if not treatment.empty and "ART_status" in treatment.columns:
    st.bar_chart(treatment["ART_status"].value_counts())