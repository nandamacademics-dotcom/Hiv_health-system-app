import streamlit as st
import pandas as pd
from utils.sheets_utils import get_testing_data, get_treatment_data

st.title("📊 Dashboard")

# Load data from Google Sheets
testing, _ = get_testing_data()
treatment, _ = get_treatment_data()

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