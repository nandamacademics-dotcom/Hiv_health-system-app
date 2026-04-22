import streamlit as st
import pandas as pd
from utils.sheets_utils import load_worksheet_data

st.title("Patient Management")

# Load data
existing_data, sheet = load_worksheet_data("Patients")

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