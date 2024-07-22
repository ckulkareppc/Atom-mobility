import streamlit as st
from streamlit_option_menu import option_menu
import importlib.util
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
from st_aggrid import AgGrid

# Main Home Page
st.title("Atom Mobility Dashboard")

st.write("Welcome to the Atom Mobility Dashboard! Find your all information here.")

# Function to load a page
def load_page(page_name):
    spec = importlib.util.spec_from_file_location(page_name, f'{page_name}.py')
    page = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(page)
    page.main()

# Create the navigation menu
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", "Total", "Generic", "Ride Hailing", "Car Rental"],
        icons=["house", "file-earmark", "file-earmark"],
        menu_icon="cast",
        default_index=0,
    )

# Total
if selected == "Home":
    st.title("Home Page")
    st.write("Welcome to the home page!")
elif selected == "Total":
    load_page("Total")
elif selected == "Generic":
    load_page("Generic")
elif selected == "Ride Hailing":
    load_page("hailing")
elif selected == "Car Rental":
    load_page("rental")
