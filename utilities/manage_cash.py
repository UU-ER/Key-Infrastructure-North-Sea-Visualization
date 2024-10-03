import streamlit as st
from pathlib import Path
import pandas as pd

from .read_data import read_results_from_h5

def show_sidebar():
    """
    Shows cash status and button in sidebar
    """
    clear_cash()
    show_cash_status()

def show_cash_status():
    """
    Displays the cash status
    :return:
    """
    if st.session_state['Result1']:
        st.sidebar.success("Results 1 successfully loaded")
    else:
        st.sidebar.error("Results 1 not loaded")

def clear_cash():
    """
    Clears cash
    :return:
    """
    if st.sidebar.button('Reset data'):
        st.session_state['Result1'] = {}

def load_data_in_cash():
    """
    Loads results into cash
    :return:
    """
    st.markdown("**Load result file**")
    uploaded_h5 = st.file_uploader("Load a result h5 file")
    if uploaded_h5 is not None:
        st.session_state['Result1'] = read_results_from_h5(uploaded_h5)

def load_cash():
    if 'Result1' not in st.session_state:
        st.session_state['Result1'] = {}
    if 'NodeLocations' not in st.session_state:
        st.session_state['NodeLocations'] = pd.read_csv("./data/Node_Locations.csv",
                                                        sep=";", index_col=0)
    if 'Summary2030' not in st.session_state:
        st.session_state['Summary2030'] = pd.read_csv("./data/Summary_2030.csv",
                                                      sep=";")
    if 'Summary2040' not in st.session_state:
        st.session_state['Summary2040'] = pd.read_csv("./data/Summary_2040.csv",
                                                      sep=";")
    if 'HeaderKeys' not in st.session_state:
        st.session_state['HeaderKeys'] = pd.read_csv("./data/HeaderKeys.csv",
                                                     sep=";")

