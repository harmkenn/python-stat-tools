import streamlit as st
import plotly_express as px
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pingouin as pg

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
    chart_choice = st.sidebar.radio("",["Histogram","Boxplot & Dotplot","QQplot","Scatterplot"])
    
    
    if chart_choice == "Histogram":
        with top[1]:
            x = st.selectbox('X-Axis', options=numeric_columns)
            cv = st.selectbox("Color", options=non_numeric_columns)
            bins = st.slider("Bin Width", min_value=1,max_value=20, value=7)
                              
        if cv != None:
            fig = px.histogram(df, x = x, color = cv, marginal = 'rug',nbins=bins, facet_row=cv, template= 'simple_white')
        else:
            fig = px.histogram(df, x = x, marginal = 'rug',nbins=bins)
        with top[1]:
            st.plotly_chart(fig, use_container_width=True)    
        
    if chart_choice == "Boxplot & Dotplot":
        with top[1]:
            x = st.selectbox('X-Axis', options=numeric_columns)
            cv = st.selectbox("Color", options=non_numeric_columns)
        if cv != None:
            fig = px.box(df, x=x, y=cv, points="all",color=cv)
        else:
            fig = px.box(df, x=x, points="all")
        with top[1]:
            st.plotly_chart(fig, use_container_width=True)    
         
    if chart_choice == "QQplot":
        with top[1]:
            y = st.selectbox('Y-Axis', options=numeric_columns)
            cv = st.selectbox("Color", options=non_numeric_columns)
            
        if cv != None:
            allcat = list(df[cv].unique())
            with top[1]:
                cat1 = st.selectbox('Category',options=allcat) 
            ny = df[df[cv]==cat1][y]

        else:
            ny = df[y]
 
        with top[1]:
            # Create a QQ-plot with confidence interval bands
            fig, ax = plt.subplots()
            ax = pg.qqplot(ny, dist='norm', confidence=.95)

            # Add labels and title
            ax.set_xlabel('Theoretical Quantiles')
            ax.set_ylabel('Sample Quantiles')
            ax.set_title('QQ-Plot with Confidence Interval Bands')
            st.pyplot(fig, use_container_width=True)    
            
    if chart_choice == "Scatterplot":
        with top[1]:
            x = st.selectbox('X-Axis', options=numeric_columns)
            y = st.selectbox('Y-Axis', options=numeric_columns, index = 1)
            cv = st.selectbox("Color", options=non_numeric_columns)
        if cv != None:
            fig = px.scatter(df, x = x, y = y, color = cv, trendline='ols')  
        else:
            fig = px.scatter(df, x = x, y = y, trendline='ols') 
        with top[1]:
            st.plotly_chart(fig, use_container_width=True) 
    

        

    with top[0]:
        st.write(df)
    
    
    with bottom[0]:
        st.write(df.describe().T)
        if cv != None:
            st.write(df.groupby([cv]).describe())
    
