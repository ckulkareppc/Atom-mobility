import streamlit as st
from streamlit_option_menu import option_menu

# Main Home Page
st.title("Atom Mobility Dashboard")

st.write("Welcome to the Atom Mobility Dashboard! Find your all information here.")

# Create the navigation menu
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", "Total", "Generic", "Ride Hailing", "Car Rental"],
        icons=["house", "file-earmark", "file-earmark"],
        menu_icon="cast",
        default_index=0,
    )

# Home Page
if selected == "Home":
    st.title("Home Page")
    st.write("Welcome to the home page!")

# Page 1
elif selected == "Page 1":
    st.title("Page 1")
    st.write("Welcome to Page 1!")

# Page 2
elif selected == "Page 2":
    st.title("Page 2")
    st.write("Welcome to Page 2!")