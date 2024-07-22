import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objs as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from st_aggrid import AgGrid

st.title('Atom Mobility Results Dashboard')

# Load credentials from st.secrets
creds_dict = st.secrets["google_sheets_credentials"]
    
# Set up the Google Sheets API client
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1yEnYDfBF2flJpVhcRHVHcgttRBMaCrUphqBSjoOezns/edit?usp=sharing')
worksheet = spreadsheet.worksheet("Total")
data = worksheet.get_all_values()

# Convert the data to a DataFrame
df = pd.DataFrame(data)


