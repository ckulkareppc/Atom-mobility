
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
worksheet = spreadsheet.worksheet("Car Rental")
data = worksheet.get_all_values()

# Convert the data to a DataFrame
df = pd.DataFrame(data)

df = df.T
df.columns = df.iloc[0]
df = df[1:]
df['Month'] = df.index
df.reset_index(drop=True, inplace=True)

df1 = pd.concat([df.iloc[:, 0:9], df.iloc[:, -1]], axis=1)
columns = ['Month'] + [col for col in df1 if col != 'Month']
df1 = df1[columns]
df1 = df1.fillna(0)


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

df2 = pd.concat([df.iloc[:, 10:22], df.iloc[:, -1]], axis=1)
df2= df2.iloc[:, 2:15]
df2 = df2.iloc[5:]
df2 = df2.fillna(0)
columns2 = ['Month'] + [col for col in df2 if col != 'Month']
df2 = df2[columns2]



# Add the year to the month column starting from 2022
start_year = 2023
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
y_columns1 = list(df1.columns[1:])  # Skip 'Month' column
y_columns2 = list(df2.columns[1:])  # Skip 'Month' column

# Create the Plotly figures
fig1 = px.line(df1, x='Month', y=y_columns1, title='Google PPC Results - Total')
fig2 = px.line(df2, x='Month', y=y_columns2, title='Google PPC Results - Remarketing')

# Select the last two rows
last_two_months = df1.tail(2)
y_columns3 = list(last_two_months.columns[1:])  # Skip 'Month' column

# Prepare data for plotting
trace_data = []
for col in last_two_months.columns:
    if col != 'Month':
        trace = go.Bar(x=last_two_months['Month'], y=last_two_months[col], name=col)
        trace_data.append(trace)

# Layout
layout = go.Layout(
    title='Last two months',
    xaxis=dict(title='Month'),
    yaxis=dict(title='Values'),
    barmode='group'
)

fig3 = go.Figure(data=trace_data, layout=layout)

# User column selection
st.subheader('Total Results')
selected_columns1 = st.multiselect('Select columns for Total Results', y_columns1, default=y_columns1[:2])
if selected_columns1:
    fig1 = px.line(df1, x='Month', y=selected_columns1, title='Google PPC Results - Total', height=600, width=800)
    st.plotly_chart(fig1)
    AgGrid(df1)

st.subheader('Remarketing Results')
selected_columns2 = st.multiselect('Select columns for Remarketing Results', y_columns2, default=y_columns2[:2])
if selected_columns2:
    fig2 = px.line(df2, x='Month', y=selected_columns2, title='Google PPC Results - Remarketing', height=600, width=800)
    st.plotly_chart(fig2)
    AgGrid(df2)

# Select the last two rows
last_two_months = df1.tail(2)
y_columns3 = list(last_two_months.columns[1:])  # Skip 'Month' column

st.subheader('Last two months')
selected_columns3 = st.multiselect('Select columns for Last two months', y_columns3, default=y_columns3[:2])
if selected_columns3:
    trace_data = []
    for col in selected_columns3:
        trace = go.Bar(x=last_two_months['Month'], y=last_two_months[col], name=col)
        trace_data.append(trace)

    # Layout
    layout = go.Layout(
        title='Last two months',
        xaxis=dict(title='Month'),
        yaxis=dict(title='Values'),
        barmode='group',
        height=600,
        width=800
    )

    fig3 = go.Figure(data=trace_data, layout=layout)
    st.plotly_chart(fig3)
    AgGrid(last_two_months)
