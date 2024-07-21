import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
import toml
import json

load_dotenv()

# Authentication function
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["general"]["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    
    st.title('Atom Mobility Results Dashboard')

    creds_toml = os.getenv('google_sheets_credentials')

    # Check if the environment variable is loaded properly
    if creds_toml is None:
        st.error("Environment variable 'GOOGLE_APPLICATION_CREDENTIALS_TOML' not found.")
    else:
        try:
            creds_dict = toml.loads(creds_toml)
        except TypeError as e:
            st.error(f"Error loading TOML data: {e}")
        else:
            # Convert TOML dictionary to JSON string and then to a dictionary
            creds_json = json.dumps(creds_dict)
            creds_dict = json.loads(creds_json)
    

    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1yEnYDfBF2flJpVhcRHVHcgttRBMaCrUphqBSjoOezns/edit?usp=sharing')

    
    
    
    

