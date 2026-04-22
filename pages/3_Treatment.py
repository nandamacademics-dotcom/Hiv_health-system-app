import streamlit as st
import pandas as pd
from utils.sheets_utils import get_patients_data, get_treatment_data

st.title("💊 Treatment Tracking")

# Load patients and treatment data
patients_df, _ = get_patients_data()
treatment_df, treatment_sheet = get_treatment_data()

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