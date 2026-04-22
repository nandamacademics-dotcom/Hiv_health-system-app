import streamlit as st
import pandas as pd
from utils.sheets_utils import get_facilities_data

st.title("Facilities")

# Load facilities data
facilities_df, facilities_sheet = get_facilities_data()

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