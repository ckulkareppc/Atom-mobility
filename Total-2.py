import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authentication function
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["general"]["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    
    st.title('Atom Mobility Results Dashboard')

    # Load credentials from st.secrets
    creds_dict = st.secrets["google_sheets_credentials"]
    
    # Set up the Google Sheets API client
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(credentials)
    
    # Open the spreadsheet
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1yEnYDfBF2flJpVhcRHVHcgttRBMaCrUphqBSjoOezns/edit?usp=sharing')
    worksheet = spreadsheet.worksheet("Total")
    data = worksheet.get_all_values()
    
    # Convert the data to a DataFrame and set headers
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # Data Cleaning
    def clean_and_convert(df):
        def clean_value(value):
            if isinstance(value, str):
                value = value.replace('€', '').replace(',', '').replace(' ', '').replace('%', '')
                if value == '?':
                    value = '0'
                try:
                    return float(value)
                except ValueError:
                    return np.nan
            return value

        for col in df.columns:
            if col != 'Month':
                df[col] = df[col].apply(clean_value)
        return df
    
    df = clean_and_convert(df)
    
    # Add Year to Month
    def add_year_to_month(df, start_year=2022):
        months = df['Month'].tolist()
        new_months = []
        year = start_year
        for month in months:
            new_months.append(f"{month} {year}")
            if month == 'December':
                year += 1
        df['Month'] = new_months
        return df
    
    df = add_year_to_month(df)
    
    # Create Plotly figures
    y_columns = list(df.columns[1:])
    fig = px.line(df, x='Month', y=y_columns, title='Google PPC Results')
    
    st.plotly_chart(fig)
    st.write(df)
