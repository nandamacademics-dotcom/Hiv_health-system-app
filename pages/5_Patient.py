import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.title("Patient Management")

# Connect to Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file("hiv-health-system-app-7ffa50f21021.json", scopes=scope)
client = gspread.authorize(creds)

sheet = client.open_by_key("1kgbCBC0jzEsmMdyrCpw1uHtF33qhMGmwQRlSNrUau10").worksheet("Patients")

# Load data
data = sheet.get_all_records()
existing_data = pd.DataFrame(data)
existing_data.columns = existing_data.columns.str.strip()  # Remove whitespace from column names

# Inputs
name = st.text_input("Name")
sex = st.selectbox("Sex", ["Male", "Female"])
age = st.number_input("Age", 0, 120)

# Save
if st.button("Save Patient", key="save_patient"):

    if name.strip() == "":
        st.error("Name is required")

    elif age <= 0:
        st.error("Age must be greater than 0")

    else:
        new_row = [
            len(existing_data) + 1,
            name,
            sex,
            age
        ]

        sheet.append_row(new_row)

        st.success("✅ Patient added successfully")

        st.rerun()

# Display
st.subheader("Patient List")
st.dataframe(existing_data)
creds = Credentials.from_service_account_file(
    "hiv-health-system-app-7ffa50f21021.json",
    scopes=scope
)