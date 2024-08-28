import streamlit as st
from pathlib import Path

from utilities import *

# Page Setup
st.set_page_config(
    page_title="Compare Scenarios",
)

scenarios = ["Baseline", "Storage", "Grid Expansion", "Hydrogen", "Synergies"]

case_keys = {"costs": "costs",
             "net emissions": "emissions_net",
             "costs at emission target (only available for energy storage)":
                 "costs_emissionlimit"}

year_selected = st.selectbox("Select target year", [2030, 2040])
case_selected = st.selectbox("Select optimization", case_keys.keys())
scenarios_selected = st.multiselect("Select scenarios to compare", scenarios)
variables_available = st.session_state["HeaderKeys"].dropna().sort_values(
    by=["Key"]).set_index([
    "Key"])["Header"].to_dict()

units = st.session_state["HeaderKeys"].dropna().sort_values(
    by=["Key"]).set_index([
    "Key"])["Unit"].to_dict()

variables_selected = st.multiselect("Select variable to plot", variables_available)
stack_cols = st.checkbox("Stack Columns")

# Take correct year:
summary_df = st.session_state["Summary" + str(year_selected)]

# Take correct results
plot_data = summary_df[summary_df["objective"] == case_keys[case_selected]]
# Filter for correct cases
plot_data = plot_data[summary_df["Case"].isin(scenarios_selected)]

# Filter for correct columns
cols = ["Case", "Subcase"]
cols.extend([variables_available[key] for key in variables_selected])
plot_data = plot_data[cols]
# Rename cols
plot_data = plot_data.fillna(0)
plot_data['Case_Subcase'] = plot_data['Case'] + ' - ' + plot_data['Subcase']
plot_data = plot_data.drop(columns=["Case", "Subcase"])
plot_data = plot_data.rename(columns={y: x for x, y in variables_available.items()})

plot_data = plot_data.melt(id_vars=["Case_Subcase"])

unit_to_show = [units[key] for key in variables_selected]
unit_to_show = " / ".join(unit_to_show)

if stack_cols:
    chart = alt.Chart(plot_data).mark_bar().encode(
        y=alt.Y('Case_Subcase:N', title=None),
        x=alt.X('value:Q', title=unit_to_show),
        color=alt.Color('variable',
                        legend=alt.Legend()
                        )
    ).interactive()
else:
    chart = (alt.Chart(plot_data).mark_bar().encode(
        y=alt.Y('variable:N', title=None),
        x=alt.X('value:Q', title=unit_to_show),
        color=alt.Color('variable',
                        legend=alt.Legend()
                        ),
        row = alt.Row('Case_Subcase:N', title="")
    ).properties(
        height=90
    ).interactive())

st.altair_chart(chart, theme="streamlit", use_container_width=True)








