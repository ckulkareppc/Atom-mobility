import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objs as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from st_aggrid import AgGrid


# Load credentials from st.secrets
creds_dict = st.secrets["google_sheets_credentials"]
    
# Set up the Google Sheets API client
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1yEnYDfBF2flJpVhcRHVHcgttRBMaCrUphqBSjoOezns/edit?usp=sharing')
worksheet = spreadsheet.worksheet("Sharing/Generic")
data = worksheet.get_all_values()

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Optionally, set the first row as the header
df.columns = df.iloc[0]
df = df[1:]

# Reset the index
df.reset_index(drop=True, inplace=True)

# Set the first column as the headers
df.columns = df.iloc[0]
df = df[1:]
df = df.T.reset_index()
df.columns = df.iloc[0]
df = df[1:]

df = df.rename(columns={'Google PPC': 'Month'})

# Create the first DataFrame up to column 'A'
df1 = df.loc[:, :'Cost per Offline Conversion']

# Add the year to the month column starting from 2022
start_year = 2022
months = df1['Month'].tolist()

# Generate the new month-year strings
new_months = []
year = start_year
for month in months:
    new_months.append(f"{month} {year}")
    if month == 'December':
        year += 1

# Update the 'Month' column
df1['Month'] = new_months

df2 = df.loc[:, 'Remarketing':]
df2 = df2.rename(columns={'Remarketing': 'Month'})

# Add the year to the month column starting from 2022
start_year = 2022
months = df2['Month'].tolist()

# Generate the new month-year strings
new_months = []
year = start_year
for month in months:
    new_months.append(f"{month} {year}")
    if month == 'December':
        year += 1

# Update the 'Month' column
df2['Month'] = new_months

def clean_and_convert(df):
    def clean_value(value):
        if isinstance(value, str):
            value = value.replace('€', '').replace(',', '').replace(' ', '').replace('%', '')
            if value == '?':
                value = '0'
            try:
                return float(value)
            except ValueError:
                return np.nan  # if conversion fails, return NaN
        return value

    for col in df.columns:
        if col != 'Month':
            df[col] = df[col].apply(clean_value)
    return df

df1 = clean_and_convert(df1)
df2 = clean_and_convert(df2)

df1 = df1.fillna(0)
df2 = df2.fillna(0)

df1['Month'] = df1['Month'].astype(str)
df2['Month'] = df2['Month'].astype(str)

# Ensure columns are properly passed as lists
#y_columns1 = list(df1.columns[1:])  # Skip 'Month' column
#y_columns2 = list(df2.columns[1:])  # Skip 'Month' column

# Create the Plotly figures
fig1 = px.line(df1, x='Month', y=y_columns1, title='Google PPC Results - Total')
fig2 = px.line(df2, x='Month', y=y_columns2, title='Google PPC Results - Remarketing')






