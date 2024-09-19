import streamlit as st
import pandas as pd
import plotly.figure_factory as pff



# Add histogram data
# https://docs.google.com/spreadsheets/d/1RYn7555m-q5gVXb9Kyp1AzteOkrUgdon3DHfkbEljT0/edit?usp=sharing
gs_URL = st.text_input("Public Google Sheet URL:","https://docs.google.com/spreadsheets/d/1RYn7555m-q5gVXb9Kyp1AzteOkrUgdon3DHfkbEljT0/edit#gid=0") 
googleSheetId = gs_URL.split("spreadsheets/d/")[1].split("/edit")[0]
worksheetName = st.text_input("Sheet Name:","Bivariate")
URL = f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={worksheetName}'
df = pd.read_csv(URL)
df = df.dropna(axis=1, how="all")

# Group data together
cq = df.pivot(columns='Gender',values='Height')

# Create distplot with custom bin_size
fig = pff.create_distplot([cq[c].dropna() for c in cq.columns], cq.columns)

# Plot!
st.plotly_chart(fig, use_container_width=True)