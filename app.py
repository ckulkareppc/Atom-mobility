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

    credentials_file_path = 'atom-404416-23dbcd33bb65.json'

    # Define the scope for the Google Sheets API
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    try:
        # Load credentials from the JSON file
        creds = Credentials.from_service_account_file(credentials_file_path, scopes=scopes)
    
        # Authorize the client
        client = gspread.authorize(creds)
    
        # Print success message
        print("Google Sheets client authorized successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1yEnYDfBF2flJpVhcRHVHcgttRBMaCrUphqBSjoOezns/edit?usp=sharing')

    
    
    
    

