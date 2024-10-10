import pandas as pd
import streamlit as st
from pathlib import Path

from utilities.process_data import export_csv
from utilities import load_cash
import altair as alt

# Session States
load_cash()

# Page Setup
st.set_page_config(
    page_title="Compare Scenarios",
)

st.header("Compare Scenarios")

scenarios = ["Baseline", "Storage", "Grid Expansion", "Hydrogen", "Synergies"]

case_keys = {}
case_keys["2030"] = {"costs": "costs",
             "net emissions": "emissions_net"}
# case_keys["2030"] = {"costs": "costs",
#              "net emissions": "emissions_net",
#              "costs at emission target (only available for energy storage)":
#                  "costs_emissionlimit"}
case_keys["2040"] = {"costs": "costs"}

with st.expander("Explanations"):
    st.subheader("Target year")
    st.markdown("The scenarios were run for 2030 and 2040. The difference is an "
                "increased hydrogen and electricity demadn in 2040.")
    st.subheader("Optimization")
    st.markdown("**Costs** optimizations minimize total system costs, composed of "
        "fixed and variable costs of the baseline (exiting) system and costs of new "
        "technologies (investment, fixed and variable). \n\n In the **net emissions** "
        "optimization, net emissions are minimized. Costs are not part of the "
        "objective function and as such, technology sizes and variables related "
        "to costs are not shown in the figure below.")
    st.subheader("Scenarios")
    st.markdown("In the **Baseline** scenario for 2030, no additional technologies "
                "can be build, and only the operation is optimized. For 2040, "
                "the existing system of 2030 is in place, but onshore wind, offshore "
                "wind and PV capacities can be expanded. Also park-to-shore cables "
                "for new offshore wind parsk are allowed. \n\n"
                "In the **Storage** scenarios, new electricity storage (onshore and "
                "offshore can be build, additionally to the existing system. \n\n"
                "In the **grid expansion scenarios**, new electricity lines (AC and "
                "DC) are allowed along various new corridors. The existing grid is "
                "also part of the scenarios. \n\n"
                "In the **hydrogen** scenarios, electrolysis, hydrogen storagen and "
                "transport and fuel cells are allowed to be build. Produced hydrogen "
                "can either be used directly in industry as a replacement for blue "
                "hydrogen or it can be reconverted into electricity (partly in "
                "existing gas turbines, up to 5% or in new fuel cells).\n\n"
                "The **synergies** scenario combines all other scenarios.")

# Year, case, scenario
year_selected = st.selectbox("Select target year", [2030, 2040])
case_selected = st.selectbox("Select optimization", case_keys[str(year_selected)].keys())
# if case_selected == "costs at emission target (only available for energy storage)":
#     scenarios = ["Storage"]
scenarios_selected = st.multiselect("Select scenarios to compare", scenarios)

# Variable
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

# Data processing
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


export_csv(
    plot_data,
    "Download shown data",
    "ScenarioComparison.csv",
)

# merge with units
units_merge =  st.session_state["HeaderKeys"].dropna().sort_values(
    by=["Key"]).set_index([
    "Key"])["Unit"]

plot_data = plot_data.merge(units_merge, right_index=True, left_on="variable")

unit_to_show = [units[key] for key in variables_selected]
unit_to_show = list(set(unit_to_show))
unit_to_show = " / ".join(unit_to_show)

if unstack_cols:
    chart = (alt.Chart(plot_data).mark_bar().encode(
        y=alt.Y('Case_Subcase:N', title=None,
                axis=alt.Axis(labelLimit=200)
                ),
        x=alt.X('value:Q', title=unit_to_show),
        color=alt.Color('variable',
                        legend=alt.Legend(title=None, orient="top", columns=1,
                                          labelLimit=500)
                        ),
        row = alt.Row('Case_Subcase:N', title="", spacing=90),
        tooltip = [alt.Tooltip('Case_Subcase:N', title="Sub-scenario"),
                   alt.Tooltip('variable:N', title="Vairable"),
                   alt.Tooltip('value:Q', title="Value"),
                   alt.Tooltip('Unit:N', title="Unit")]
    ).properties(
    ).interactive())
else:
    chart = alt.Chart(plot_data).mark_bar().encode(
        y=alt.Y('Case_Subcase:N', title=None,
                axis=alt.Axis(labelLimit=200)
                ),
        x=alt.X('value:Q', title=unit_to_show),
        color=alt.Color('variable',
                        legend=alt.Legend(title=None, orient="top", columns=1,
                                          labelLimit=500)
                        ),
        tooltip = [alt.Tooltip('Case_Subcase:N', title="Sub-scenario"),
                   alt.Tooltip('variable:N', title="Variable"),
                   alt.Tooltip('value:Q', title="Value"),
                   alt.Tooltip('Unit:N', title="Unit")]
    ).interactive()

st.altair_chart(chart, theme="streamlit", use_container_width=True)








