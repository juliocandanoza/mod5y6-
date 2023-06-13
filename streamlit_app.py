import pandas as pd
import plotly.express as px
import streamlit as st

data = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv") 
st.title("San Francisco Crime Map")
st.sidebar.header("Options")
filtered_data = data  
fig = px.scatter_mapbox(
    filtered_data,
  
    lat="Latitude",  
    lon="Longitude",  
    hover_name="Incident Category",  
    color="Incident Category",  
    zoom=10
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig)
