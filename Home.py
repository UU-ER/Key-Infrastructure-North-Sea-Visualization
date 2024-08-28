import streamlit as st

from utilities import *
# from pathlib import Path
# import h5py
# import pandas as pd
# from utilities import *
# from networks import plot_nodes
# import folium
# from streamlit_folium import st_folium
# from branca.colormap import linear
# from folium.plugins import PolyLineTextPath, PolyLineOffset
# import sys

# Session States
if 'Result1' not in st.session_state:
    st.session_state['Result1'] = {}
if 'NodeLocations' not in st.session_state:
    st.session_state['NodeLocations'] = pd.read_csv("./data/Node_Locations.csv",
                                                    sep=";", index_col=0)
if 'Summary2030' not in st.session_state:
    st.session_state['Summary2030'] = pd.read_excel("./data/Summary_2030.xlsx")
if 'Summary2030' not in st.session_state:
    st.session_state['Summary2040'] = pd.read_excel("./data/Summary_2040.xlsx")
if 'HeaderKeys' not in st.session_state:
    st.session_state['HeaderKeys'] = pd.read_excel("./data/HeaderKeys.xlsx")
# Page Setup
st.set_page_config(
    page_title="Home",
)

# Show cash status
show_sidebar()

st.write("Welcome to the visualization platform of the paper PAPERNAME! 👋")
st.write("Select an option on the left.")
