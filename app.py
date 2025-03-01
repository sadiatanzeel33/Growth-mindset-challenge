import streamlit as st
import pandas as pd
import os
import base64
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')
st.markdown("""
    <style>
        body, .main, .stApp {
            background-color: #ffffff;
            color: #000000;
        }
        .sidebar .sidebar-content {
            background-color: #f1f1f1;
            color: #000000;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: #ffffff;
            border: none;
            border-radius: 5px;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .stTextInput > div > div > input:focus {
            background-color: #f1f1f1;
            color: #000000;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #000000;
        }
        .dataframe {
            background-color: #f1f1f1;
            color: #000000;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .stDataFrame thead {
            background-color: #f1f1f1;
            color: #000000;
        }
        .stDataFrame tbody {
            background-color: #ffffff;
        }
        .stDataFrame tbody tr:hover {
            background-color: #f1f1f1;
        }
        .icon-container {
            display: flex;
            align-items: center;
        }
        .icon-container img {
            width: 50px;
            height: auto;
            margin-right: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="icon-container"><img src="https://img.icons8.com/fluency/50/000000/broom.png" alt="Broom Icon"><h1>Data Sweeper</h1></div>', unsafe_allow_html=True)

st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024:.2f} KB")

        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Filled!")

        st.subheader("Download Cleaned Data")
        if st.button("Download CSV"):
            towrite = BytesIO()
            df.to_csv(towrite, index=False)
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{file.name}_cleaned.csv">Download CSV file</a>'
            st.markdown(href, unsafe_allow_html=True)

        if st.button("Download Excel"):
            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='xlsxwriter')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file.name}_cleaned.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True)
