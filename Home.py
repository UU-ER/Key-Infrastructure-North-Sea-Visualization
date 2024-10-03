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
load_cash()

# Page Setup
st.set_page_config(
    page_title="Home",
)

# Show cash status
# show_sidebar()

st.write("Welcome to the visualization platform of the paper PAPERNAME! 👋")
st.write("On the page 'Compare Scenarios' you can compare the results for the 2030 "
         "and 2040 scenarios for selected variables. On the page 'Download Data', "
         "you can download the aggregated results for the two years")
