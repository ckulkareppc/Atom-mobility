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

    # Main Home Page
    st.title("Atom Mobility Dashboard")
    
    st.write("Welcome to the Atom Mobility Dashboard! Find your all information here.")
    
    def load_page(file_name):
    with open(file_name, "r") as file:
        code = file.read()
    exec(code, globals())
    
    # Create the navigation menu
    with st.sidebar:
        selected = option_menu(
            "Main Menu",
            ["Home", "Total", "Generic", "Ride Hailing", "Car Rental"],
            icons=["file-earmark", "file-earmark"],
            menu_icon="cast",
            default_index=0,
        )

    # All pages
    if selected == "Home":
        st.title("Home Page")
        st.write("Welcome to the home page!")
    elif selected == "Total":
        load_page("Total.py")
    elif selected == "Generic":
        load_page("Generic")
    elif selected == "Ride Hailing":
        load_page("hailing")
    elif selected == "Car Rental":
        load_page("rental")
    

