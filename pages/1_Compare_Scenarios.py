import streamlit as st
from pathlib import Path

from utilities import *

# Page Setup
st.set_page_config(
    page_title="Compare Scenarios",
)

scenarios = ["Baseline", "Storage"]
summary_df = st.session_state["Summary"]

year_selected = st.selectbox("Select target year", [2030, 2040])
case_selected = st.selectbox("Select optimization", ["costs", "net emissions"])
scenarios_selected = st.multiselect("Select scenarios to compare", scenarios)
variables_selected = st.selectbox("Select variable to plot", summary_df.columns)

# Filter for correct columns
cols = ["Case", "Subcase"]
cols.extend([variables_selected])
plot_data = summary_df[cols]

# Filter for correct cases
plot_data = plot_data[plot_data["Case"].isin(scenarios_selected)]

plot_data.columns = ["Case", "Subcase", "value"]

chart = alt.Chart(plot_data).mark_bar().encode(
    x='Subcase',
    y='value:Q').interactive()

st.altair_chart(chart, theme="streamlit", use_container_width=True)







