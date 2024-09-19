import streamlit as st
import plotly_express as px
import pandas as pd
from plotnine import *
from plotly.tools import mpl_to_plotly as ggplotly
import numpy as np

def app():
    # title of the app
    st.markdown("Quantitative Stats")
    # Add a sidebar
    st.sidebar.subheader("Graph Settings")
    
    top = st.columns((1,1))
    bottom = st.columns(1)
    with top[0]:
        gs_URL = st.session_state.gs_URL
        googleSheetId = gs_URL.split("spreadsheets/d/")[1].split("/edit")[0]
        worksheetName = st.text_input("Sheet Name:","Bivariate")
        URL = f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={worksheetName}'
    

        if st.button('Refresh'):
            df = pd.read_csv(URL)
            df = df.dropna(axis=1, how="all")      
    df = pd.read_csv(URL)
    df = df.dropna(axis=1, how="all") 
       
    global numeric_columns
    global non_numeric_columns
    try:
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        non_numeric_columns.append(None)
        
    except Exception as e:
        print(e)
        st.write("Please upload file to the application.")
            
    # add a select widget to the side bar
    chart_choice = st.sidebar.radio("",["Histogram","Boxplot","Dotplot","QQplot","Scatterplot"])
    
    
    #y = st.sidebar.selectbox('Y-Axis', options=numeric_columns)
    
    p = ggplot(df)
    
    if chart_choice == "Histogram":
        with top[1]:
            x = st.selectbox('X-Axis', options=numeric_columns)
            cv = st.selectbox("Color", options=non_numeric_columns)
            bins = st.slider("Number of Bins", min_value=1,max_value=40, value=7)
        if cv != None:
            p = p + geom_histogram(aes(x=x, fill = cv, color = cv),position= "identity",alpha=.4, bins = bins)
        else:
            p = p + geom_histogram(aes(x=x),color="darkblue", fill="lightblue", bins = bins)
            
    if chart_choice == "Boxplot":
        with top[1]:
            x = st.selectbox('X-Axis', options=numeric_columns)
            cv = st.selectbox("Color", options=non_numeric_columns)
        if cv != None:
            p = p + geom_boxplot(aes(x=cv,y=x, fill = cv)) + coord_flip()
        else:
            p = p + geom_boxplot(aes(x=1,y=x,width=.1),color="darkblue", fill="lightblue") + coord_flip()
            
    if chart_choice == "Dotplot":
        with top[1]:
            x = st.selectbox('X-Axis', options=numeric_columns)
            cv = st.selectbox("Color", options=non_numeric_columns)
        if cv != None:
            p = p + geom_jitter(aes(x=cv,y=x, fill = cv, color = cv), size = 2, height = 0, width =.1)+ coord_flip()
        else:
            p = p + geom_jitter(aes(x=1,y=x), size = 2, height = 0, width =.1)+ coord_flip()
            
    if chart_choice == "QQplot":
        with top[1]:
            x = st.selectbox('X-Axis', options=numeric_columns)
            cv = st.selectbox("Color", options=non_numeric_columns)
        if cv != None:
            p = p + stat_qq(aes(sample=x,color=cv)) + stat_qq_line(aes(sample=x,color=cv))+ labs(x = "Theoretical Quantiles", y = "Sample Quantiles")
        else:
            p = p + stat_qq(aes(sample=x)) + stat_qq_line(aes(sample=x)) + labs(x = "Theoretical Quantiles", y = "Sample Quantiles")
            
    if chart_choice == "Scatterplot":
        with top[1]:
            x = st.selectbox('X-Axis', options=numeric_columns)
            y = st.selectbox('Y-Axis', options=numeric_columns, index = 1)
            cv = st.selectbox("Color", options=non_numeric_columns)
        if cv != None:
            p = p + geom_point(aes(x=x,y=y,color=cv))
        else:
            p = p + geom_point(aes(x=x,y=y))
    
    
    with top[1]:
        st.pyplot(ggplot.draw(p))

    with top[0]:
        st.write(df)
    
    
    with bottom[0]:
        st.write(df.describe().T)
        if cv != None:
            st.write(df.groupby([cv]).describe())
    
