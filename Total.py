import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objs as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from st_aggrid import AgGrid
from google.oauth2 import service_account
from googleapiclient.discovery import build
import re

st.title('Atom Mobility Results Dashboard')

# Load credentials from st.secrets
creds_dict = st.secrets["google_sheets_credentials"]

st.write("Google Sheets Credentials:", creds_dict)

# Convert credentials to JSON and load them
creds_json = json.dumps(creds_dict)
creds_info = json.loads(creds_json)
    
# Authenticate with Google Sheets API
creds = service_account.Credentials.from_service_account_info(creds_info)
service = build('sheets', 'v4', credentials=creds)

# Define the spreadsheet ID and range you want to access
spreadsheet_id = '1yEnYDfBF2flJpVhcRHVHcgttRBMaCrUphqBSjoOezns'
range_name = 'Sheet1!A1:D10'  # Adjust range as needed

# Make an API call to read data from Google Sheets
try:
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    if not values:
        st.write('No data found.')
    else:
        st.write('Data from Google Sheets:', values)
except Exception as e:
    st.error(f'An error occurred: {e}')



