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
creds_dict = dict(st.secrets["google_sheets_credentials"])  # Create a mutable copy of the dictionary

# Debug: Print the structure of creds_dict
st.write("Credentials Dictionary:", creds_dict)

# Ensure the private key is correctly formatted
def format_private_key(key):
    # Remove the newline characters within the private key value
    return key.replace("\\n", "\n")

# Convert TOML data (loaded as a dictionary) to JSON format
def convert_toml_to_json(toml_dict):
    if 'private_key' in toml_dict:
        toml_dict['private_key'] = format_private_key(toml_dict['private_key'])
    return json.dumps(toml_dict)

# Perform the conversion
try:
    creds_json = convert_toml_to_json(creds_dict)
    st.write("Credentials JSON:", creds_json)
except TypeError as e:
    st.error(f"TypeError: {e}")
except Exception as e:
    st.error(f"An error occurred: {e}")




