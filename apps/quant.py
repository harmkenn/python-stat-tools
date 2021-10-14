import streamlit as st
import plotly_express as px
import pandas as pd
from plotnine import *
from plotly.tools import mpl_to_plotly as ggplotly
import numpy as np

def app():
    # title of the app
    st.title("Quantitative Stats")
    # Add a sidebar
    st.sidebar.subheader("Graph Settings")
    
    gs_URL = st.text_input("Public Google Sheet URL:","https://docs.google.com/spreadsheets/d/1Fx7f6rM5Ce331F9ipsEMn-xRjUKYiR3R_v9IDBusUUY/edit#gid=0") 
    googleSheetId = gs_URL.split("spreadsheets/d/")[1].split("/edit")[0]
    worksheetName = st.text_input("Sheet Name:","Sheet1")
    URL = f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={worksheetName}'
    
    @st.cache (ttl = 600)
    def upload_gs(x):
        out = pd.read_csv(x)
        return out

    df = upload_gs(URL)
    df = df.dropna(axis=1, how="any") 
       
    global numeric_columns
    global non_numeric_columns
    try:
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        non_numeric_columns.append(None)
        print(non_numeric_columns)
    except Exception as e:
        print(e)
        st.write("Please upload file to the application.")
            
    # add a select widget to the side bar
    chart_choice = st.sidebar.radio("",["Histogram","Boxplot","Dotplot","QQPlot","Scatterplot"])
    
    
    #y = st.sidebar.selectbox('Y-Axis', options=numeric_columns)
    
    p = ggplot(df)
    
    if chart_choice == "Histogram":
        st.sidebar.subheader("Histogram Settings")
        x = st.sidebar.selectbox('X-Axis', options=numeric_columns)
        cv = st.sidebar.selectbox("Color", options=non_numeric_columns)
        bins = st.sidebar.slider("Number of Bins", min_value=1,max_value=40, value=7)
        if cv != None:
            p = p + geom_histogram(aes(x=x, fill = cv, color = cv),position= "identity",alpha=.4, bins = bins)
        else:
            p = p + geom_histogram(aes(x=x),color="darkblue", fill="lightblue", bins = bins)
    
    st.pyplot(ggplot.draw(p))
    st.write(df)
    
   
