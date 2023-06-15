import streamlit as st
import pandas as pd
import plotly as px

st.set_page_config(page_title="Reports",
                   page_icon=":cop:",
                   layout="wide"
)
df = pd.read_excel("Police_Department_Incident_Reports__2018_to_Present-2.xlsx")

# ---- SIDEBAR ----

st.sidebar.header("Filtros")
day = st.sidebar.multiselect(
    "Select the day:",
    options=df["Incident Day of Week"].unique(),
    default=df["Incident Day of Week"].unique()
)

district = st.sidebar.multiselect(
    "Select the district:",
    options=df["Police District"].unique(),
    default=df["Police District"].unique()
)

category = st.sidebar.multiselect(
    "Select the category:",
    options=df["Incident Category"].unique(),
    default=df["Incident Category"].unique()
)

df_selection = df.query(
    "`Incident Day of Week` == @day and `Police District` == @district and `Incident Category` == @category"
)

st.dataframe(df_selection)


# ---- MAINPAGE ------

st.title(":cop: KPI's Reports")
st.markdown("##")

# TOP KPI´s
conteo_district = df_selection['Police District'].value_counts()

porcentaje = conteo_district/len(df['Police District']) * 100

conteo_dia = df_selection['Incident Day of Week'].value_counts()



first_column, second_column, third_column = st.columns(3)

with first_column:
    st.subheader("Total robberies by district")
    st.subheader(conteo_district)

with second_column:
    st.subheader("Percentage of robberies by district")
    st.subheader(f"{porcentaje.round(1)}")

with third_column:
    st.subheader("Total robberies per day")
    st.subheader(conteo_dia)



st.markdown("---")

# ---- Robberies per day ----

robberies_per_day = (
    df_selection.groupby('Incident Day of Week').size().reset_index(name='Total').sort_values(by="Total")
)
fig_robberies_per_day = px.bar(
    robberies_per_day,
    x="Total",
    y="Incident Day of Week",
    orientation="h",
    title="<b>Robberies per day</b>",
    color_discrete_sequence=["#EF280F"] * len(robberies_per_day),
    template="plotly_white"
)

categories = (
    df_selection.groupby('Incident Subcategory').size().reset_index(name='Total').sort_values(by="Total")
)
fig_robberies_subcategories = px.bar(
    categories,
    x="Total",
    y="Incident Subcategory",
    orientation="h",
    title="<b>Robberies by Subcategory</b>",
    color_discrete_sequence=["#024A86"] * len(categories),
    template="plotly_white"
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_robberies_per_day, use_container_width=True)
right_column.plotly_chart(fig_robberies_subcategories, use_container_width=True)

# Esconder streamlit style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)
