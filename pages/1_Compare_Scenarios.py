import streamlit as st
from pathlib import Path

from utilities import *

# Page Setup
st.set_page_config(
    page_title="Compare Scenarios",
)

scenarios = ["Baseline", "Storage", "Grid Expansion", "Hydrogen", "Synergies"]

case_keys = {}
case_keys["2030"] = {"costs": "costs",
             "net emissions": "emissions_net",
             "costs at emission target (only available for energy storage)":
                 "costs_emissionlimit"}
case_keys["2040"] = {"costs": "costs"}

year_selected = st.selectbox("Select target year", [2030, 2040])
case_selected = st.selectbox("Select optimization", case_keys[str(year_selected)].keys())
scenarios_selected = st.multiselect("Select scenarios to compare", scenarios)

all_vars = st.session_state["HeaderKeys"]
if case_selected == "net emissions":
    all_vars = all_vars[all_vars["Available for net_emissions"]==1]
if year_selected == 2030:
    all_vars = all_vars[all_vars["Available 2030"]==1]

variables_available = all_vars.dropna().sort_values(
    by=["Key"]).set_index([
    "Key"])["Header"].to_dict()

units = st.session_state["HeaderKeys"].dropna().sort_values(
    by=["Key"]).set_index([
    "Key"])["Unit"].to_dict()

variables_selected = st.multiselect("Select variable to plot", variables_available)
unstack_cols = st.checkbox("Unstack Columns")

# Take correct year:
summary_df = st.session_state["Summary" + str(year_selected)]

# Take correct results
plot_data = summary_df[summary_df["objective"] == case_keys[str(year_selected)][case_selected]]
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
if len(set(unit_to_show)) == 1:
    unit_to_show = list(set(unit_to_show))
else:
    unit_to_show = " / ".join(unit_to_show)

if unstack_cols:
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
else:
    chart = alt.Chart(plot_data).mark_bar().encode(
        y=alt.Y('Case_Subcase:N', title=None),
        x=alt.X('value:Q', title=unit_to_show),
        color=alt.Color('variable',
                        legend=alt.Legend()
                        )
    ).interactive()

st.altair_chart(chart, theme="streamlit", use_container_width=True)








