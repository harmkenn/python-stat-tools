import streamlit as st
import plotly_express as px
import pandas as pd
import numpy as np
import math
import scipy.stats as ss
from scipy.stats import *



def app():
    # add a select widget to the side bar
    #st.sidebar.subheader("Discrete Probaility")
    prob_choice = st.radio("",["Discrete Probability","Binomial Probability","Geometric Probability","Poisson Probability"])
    #st.markdown('Discrete Probability') 
    if prob_choice == "Discrete Probability":
        top = st.columns((1,1,2))
        # bottom = st.columns((1,1))
        with top[0]:
            def display_data(file_path, selected_sheet):
                try:
                    # Read data from the specified file path and sheet
                    df = pd.read_excel(file_path, sheet_name=selected_sheet)
                    
                except FileNotFoundError:
                    st.error("File not found. Please check the path and try again.")
                except (KeyError, ValueError):
                    st.error(f"Sheet '{selected_sheet}' not found in the file.")
            # Dropdown menu for sheet selection
            sheet_names = pd.read_excel(st.session_state.xlsx, sheet_name=None, nrows=0).keys()  # Get sheet names
            st.session_state.sheet = st.selectbox("Select sheet:", sheet_names, index=1)
            

            # Button to refresh data
            if st.button("Refresh Data"):
                display_data(st.session_state.xlsx, st.session_state.sheet)               
            df = pd.read_excel(st.session_state.xlsx, st.session_state.sheet)
            st.dataframe(df)
                           
            global numeric_columns
            global non_numeric_columns
            try:
                numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
                non_numeric_columns = list(df.select_dtypes(['object']).columns)
            except Exception as e:
                print(e)
                st.write("Please upload file to the application.")
        with top[1]:
            
            
            if len(non_numeric_columns) >= 1: 
                df['Mean'] = df['X']*df['Prob(X)']
                m = df.groupby(['Type'])['Mean'].sum()
                df = pd.merge(df,m,on='Type',how='inner')
                df['SD'] = (df['X']-df['Mean_y'])**2*df['Prob(X)']
                n = df.groupby(['Type'])['SD'].sum()**(1/2)
                mn = pd.concat([m,n],axis=1)
                
                st.dataframe(mn)
            
            with top[2]:
                fig = px.bar(df, x = 'X', y = 'Prob(X)', facet_row='Type', template= 'simple_white')
                st.plotly_chart(fig, use_container_width=True)
            
    
    
    if prob_choice == "Binomial Probability":
        
        top = st.columns(2)
        with top[0]:
            st.subheader("Binomial Probability")
            bip, bit, bih = st.text_input("Hit Probability:",.2),st.text_input("Tries:",8),st.text_input("Hits:",0)
            bit = int(bit)
            bip = float(bip)
            biah = np.r_[0:bit+1]
            cdf = binom.cdf(biah,bit,bip)
            pmf = binom.pmf(biah,bit,bip)
            biah = pd.DataFrame(biah)
            cdf = pd.DataFrame(cdf)
            pmf = pd.DataFrame(pmf)
            bm,bv = binom.stats(bit,bip)
            bdf = pd.concat([biah,pmf,cdf],axis=1)
            bdf.columns = ["Hits","PDF","CDF"]
        with top[1]:
            st.write(bdf)
            data = pd.DataFrame({"Mean":bm,"Std Dev":math.sqrt(bv)},index = [0])
            st.write(data)
        with top[0]:
            fig = px.bar(bdf, x = 'Hits', y = 'PDF', template= 'simple_white')
            st.plotly_chart(fig, use_container_width=True)
            

        
    if prob_choice == "Geometric Probability": 

        again = st.columns(2)    
        with again[0]:   
            st.subheader("Geometric Probability")
            gip, gih = st.text_input("Hit Probability:",.2,key ="1"),st.text_input("Tries:",4,key="2")
            gip = float(gip)
            gih = int(gih)
            giah = np.r_[0:gih+6/gip]
            cdf = geom.cdf(giah,gip)
            pmf = geom.pmf(giah,gip)
            giah = pd.DataFrame(giah)
            cdf = pd.DataFrame(cdf)
            pmf = pd.DataFrame(pmf)
            gm,gv = geom.stats(gip)
            gdf = pd.concat([giah,pmf,cdf],axis=1)
            gdf.columns = ["Hits","PDF","CDF"]
        with again[1]:
            st.write(gdf)
            data = pd.DataFrame({"Mean":gm,"Std Dev":math.sqrt(gv)},index = [0])
            st.write(data)
        with again[0]:
            fig = px.bar(gdf, x = 'Hits', y = 'PDF', template= 'simple_white')
            st.plotly_chart(fig, use_container_width=True)


    if prob_choice == "Poisson Probability":      
        again = st.columns(2)     
        with again[0]:   
            st.subheader("Poisson Probability")
            peh, pah = st.text_input("Expected Hits:",2,key ="3"),st.text_input("Actual Hits:",4,key="4")
            peh = float(peh)
            pah = int(pah)
            paah = np.r_[0:pah+peh*2]
            cdf = poisson.cdf(paah,peh)
            pmf = poisson.pmf(paah,peh)
            paah = pd.DataFrame(paah)
            cdf = pd.DataFrame(cdf)
            pmf = pd.DataFrame(pmf)
            pm,pv = poisson.stats(peh)
            pdf = pd.concat([paah,pmf,cdf],axis=1)
            pdf.columns = ["Hits","PDF","CDF"]
        with again[1]:
            st.write(pdf)
            data = pd.DataFrame({"Mean":pm,"Std Dev":math.sqrt(pv)},index = [0])
            st.write(data)
        with again[0]:
            fig = px.bar(pdf, x = 'Hits', y = 'PDF', template= 'simple_white')
            st.plotly_chart(fig, use_container_width=True)
    
    
    
    
    