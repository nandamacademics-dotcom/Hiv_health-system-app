import streamlit as st
import pandas as pd
from utils.sheets_utils import get_patients_data, get_testing_data
from datetime import date

st.title("🔬 HIV Testing")

# Load patients and testing data
patients_df, _ = get_patients_data()
testing_df, testing_sheet = get_testing_data()

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
