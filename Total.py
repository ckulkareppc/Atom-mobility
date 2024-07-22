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

# Load credentials from Streamlit secrets (already in TOML format)
creds_dict = st.secrets["google_sheets_credentials"]

# Convert TOML data (loaded as a dictionary) to JSON format
def convert_toml_to_json(toml_dict):
    return json.dumps(toml_dict)

creds_json = convert_toml_to_json(creds_dict)


