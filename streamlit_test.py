import streamlit as st
import pandas as pd
import plotly.express as px

# pickled dataframe from notebook_v4
# unpickled_df = pd.read_pickle("all_emissions_post_calc_df.pkl")
unpickled_df = pd.read_pickle("calcs_for_weeks.pkl")

st.set_page_config(page_title="Emissions",page_icon=":bar_chart:",layout="wide")

# st.dataframe(unpickled_df)

# ---- SIDEBAR ----
st.sidebar.header("Please filter here:")
fuel = st.sidebar.multiselect(
    "Select the fuel:",
    options=unpickled_df["Fuel"].unique(),
    default=unpickled_df["Fuel"].unique()
)

transport_type = st.sidebar.multiselect(
    "Select the transport type:",
    options=unpickled_df["Transport_Type"].unique(),
    default=unpickled_df["Transport_Type"].unique()
)

df_selection = unpickled_df.query(
    "Fuel == @fuel & Transport_Type == @transport_type"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Emissions Dashboard")
st.markdown("##") # just to separate new paragraph (markdown field)

# ---- TOP KPI's ----
yearly_distance = int(df_selection["Yearly Distance Miles"].sum())
yearly_co2e = int(df_selection["Yearly CO2e"].sum())
yearly_journeys = int(df_selection["Total Journeys"].sum())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Yearly distance (miles)")
    st.subheader(f"{yearly_distance:,}")
with middle_column:
    st.subheader("Yearly Journeys")
    st.subheader(f"{yearly_journeys:,}")
with right_column:
    st.subheader("Yearly CO2e emissions (KG)")
    st.subheader(f"{yearly_co2e:,}")

st.markdown("- - -")

# ---- Distance by fuel type [Bar chart] ----
distance_by_fueltype = (
    df_selection.groupby(by=["Fuel"]).sum()[["Distance_Miles"]].sort_values(by="Distance_Miles")
)

fig_distance_by_fueltype = px.bar(
    distance_by_fueltype,
    x="Distance_Miles",
    y=distance_by_fueltype.index,
    # hover_data={'Distance_Miles':':.2f'},
    labels={"Distance_Miles": "Distance (Miles)"}, #because the underscore looks meh
    orientation="h",
    title="<b>Distance (Miles) by fuel</b>",
    color_discrete_sequence=["#0083B8"] * len(distance_by_fueltype),
    template="plotly_white"
)

fig_distance_by_fueltype.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    # xaxis=(dict(showgrid=False))
)

# ---- Yearly Journeys [Bar chart] ----
journeys_by_fueltype = (
    df_selection.groupby(by=["Fuel"]).sum()[["Total Journeys"]].sort_values(by="Total Journeys")
)

fig_journeys_by_fueltype = px.bar(
    journeys_by_fueltype,
    x="Total Journeys",
    y=journeys_by_fueltype.index,
    orientation="h",
    title="<b>Journeys by fuel</b>",
    color_discrete_sequence=["#0083B8"] * len(journeys_by_fueltype),
    template="plotly_white"
)

fig_journeys_by_fueltype.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    # xaxis=(dict(showgrid=False))
)

# ---- CO2e by fuel type [Bar chart] ----
co2e_by_fueltype = (
    df_selection.groupby(by=["Fuel"]).sum()[["kg CO2e"]].sort_values(by="kg CO2e")
)

fig_co2e_by_fueltype = px.bar(
    co2e_by_fueltype,
    x="kg CO2e",
    y=co2e_by_fueltype.index,
    orientation="h",
    title="<b>CO2e by fuel</b>",
    color_discrete_sequence=["#0083B8"] * len(co2e_by_fueltype),
    template="plotly_white"
)

fig_co2e_by_fueltype.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    # xaxis=(dict(showgrid=False))
)

# ---- Hide streamlit style ---- 
# Hides the top right menu button, and the "made with streamlit" at the bottom
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# left_column.plotly_chart(fig_co2e_by_fueltype, use_container_width=True)
left_column, middle_column, right_column = st.columns(3)

left_column.plotly_chart(fig_distance_by_fueltype, use_container_width=True)
middle_column.plotly_chart(fig_journeys_by_fueltype, use_container_width=True)
right_column.plotly_chart(fig_co2e_by_fueltype, use_container_width=True)

st.dataframe(df_selection)