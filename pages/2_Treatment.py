import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.title("Treatment")

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

# Load existing treatment data
treatment_sheet = sheet.worksheet("Treatment")
treatment_data = treatment_sheet.get_all_records()
treatment_df = pd.DataFrame(treatment_data)

if patients_df.empty:
    st.warning("No patients found. Please add patient first.")

else:
    # Dropdown
    patient_dict = {f"{row['patient_id']} - {row['name']}": row['patient_id'] for _, row in patients_df.iterrows()}
    selected = st.selectbox("Select Patient", list(patient_dict.keys()))

    # ✅ Define patient_id
    patient_id = patient_dict[selected]

    # Inputs
    art = st.selectbox("ART Status", ["On ART", "Not on ART"])
    pregnancy = st.selectbox("Pregnancy Status", ["Yes", "No"])

    # ✅ ONE button ONLY
    if st.button("Save Treatment", key="save_treatment_btn"):

        # Get next treatment_id
        next_treatment_id = len(treatment_df) + 1

        new_row = [
            next_treatment_id,
            patient_id,
            art,
            pregnancy
        ]

        treatment_sheet.append_row(new_row)

        st.success("✅ Treatment recorded successfully")