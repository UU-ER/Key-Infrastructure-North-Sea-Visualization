import h5py
import pandas as pd
import streamlit
import streamlit as st

@st.cache_data
def aggregate_time(df, level, aggregation = 'sum'):
    if aggregation == 'sum':
        df = df.groupby(level=level).sum()
    elif aggregation == 'mean':
        df = df.groupby(level=level).mean()
    df.index.names = ['Timeslice']
    return df


def export_csv(df, label, filename):
    """
    Makes a button that allows for csv export
    :param df: dataframe to export
    :param label: label of button
    :param filename: filename to export
    :return:
    """
    excel_buffer = df.to_csv(index=False)
    st.download_button(
        label=label,
        data=excel_buffer,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
