import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.title("Facilities")

# Connect to Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1kgbCBC0jzEsmMdyrCpw1uHtF33qhMGmwQRlSNrUau10")

# Load facilities data
facilities_sheet = sheet.worksheet("Facilities")
facilities_data = facilities_sheet.get_all_records()
facilities_df = pd.DataFrame(facilities_data)

name = st.text_input("Facility Name")
township = st.text_input("Township")
state = st.text_input("State")

if st.button("Add Facility"):
    if name.strip() and township.strip() and state.strip():
        # Get next facility_id
        next_facility_id = len(facilities_df) + 1

        new_row = [
            next_facility_id,
            name,
            township,
            state
        ]

        facilities_sheet.append_row(new_row)
        st.success("Facility added!")
        st.rerun()
    else:
        st.error("All fields are required")

st.subheader("Facilities List")
st.dataframe(facilities_df)