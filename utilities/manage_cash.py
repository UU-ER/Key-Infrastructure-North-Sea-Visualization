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
        st.session_state['NodeLocations'] = None

def load_data_in_cash():
    """
    Loads results into cash
    :return:
    """
    st.markdown("**Load result file**")
    uploaded_h5 = st.file_uploader("Load a result h5 file")
    if uploaded_h5 is not None:
        st.session_state['Result1'] = read_results_from_h5(uploaded_h5)


