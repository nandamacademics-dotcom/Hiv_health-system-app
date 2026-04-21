import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import date

st.title("HIV Testing")

# Connect to Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1kgbCBC0jzEsmMdyrCpw1uHtF33qhMGmwQRlSNrUau10")

# Load patients
patients_sheet = sheet.worksheet("Patients")
patients_data = patients_sheet.get_all_records()
patients_df = pd.DataFrame(patients_data)
patients_df.columns = patients_df.columns.str.strip()  # Remove whitespace from column names

# Load existing HIV testing data
testing_sheet = sheet.worksheet("HIV_Testing")
testing_data = testing_sheet.get_all_records()
testing_df = pd.DataFrame(testing_data)

if patients_df.empty:
    st.warning("No patients found. Please add patient first.")

else:
    # Create dropdown
    patient_dict = {f"{row['patient_id']} - {row['name']}": row['patient_id'] for _, row in patients_df.iterrows()}

    selected = st.selectbox("Select Patient", list(patient_dict.keys()))

    # ✅ DEFINE patient_id HERE (IMPORTANT)
    patient_id = patient_dict[selected]

    test_date = st.date_input("Test Date")
    result = st.selectbox("Result", ["Negative", "Positive"])

    # ✅ BUTTON INSIDE SAME BLOCK
    if st.button("Save Test"):

        # Get next test_id
        next_test_id = len(testing_df) + 1

        new_row = [
            next_test_id,
            patient_id,
            str(test_date),
            result
        ]

        testing_sheet.append_row(new_row)

        st.success("✅ Test saved successfully")

        if result == "Positive":
            st.warning("⚠ Patient is HIV Positive → Go to Treatment Page")
