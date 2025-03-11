import streamlit as st
import pandas as pd
import json
import re

def process_unstructured_data(file):
    """Process the uploaded unstructured file into structured data."""
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.json'):
        df = pd.json_normalize(json.load(file))
    elif file.name.endswith('.txt'):
        lines = file.readlines()
        data = [re.split(r'\s+', line.decode('utf-8').strip()) for line in lines if line.strip()]
        df = pd.DataFrame(data)
    else:
        st.error("Unsupported file format. Please upload a CSV, JSON, or TXT file.")
        return None
    return df

st.title("Unstructured to Structured Data Converter")

uploaded_file = st.file_uploader("Upload an unstructured data file", type=["csv", "json", "txt"])

if uploaded_file:
    st.write("### Raw File Preview")
    st.text(uploaded_file.getvalue().decode("utf-8")[:500])  # Show preview of raw content
    
    df = process_unstructured_data(uploaded_file)
    
    if df is not None:
        st.write("### Structured Data Preview")
        st.dataframe(df.head())
        
        st.download_button(
            label="Download Structured Data as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="structured_data.csv",
            mime="text/csv"
        )
