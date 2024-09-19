import streamlit as st
import plotly_express as px
import pandas as pd
from plotnine import *
from plotly.tools import mpl_to_plotly as ggplotly
import numpy as np
import math
import scipy.stats as ss
from scipy.stats import *



def app():
    # add a select widget to the side bar
    st.sidebar.subheader("Discrete Probaility")
    prob_choice = st.sidebar.radio("",["Discrete Probability","Binomial Probability","Geometric Probability","Poisson Probability"])
    st.markdown('Discrete Probability') 
    if prob_choice == "Discrete Probability":
        top = st.columns((1,1,2))
        bottom = st.columns((1,1))
        with top[0]:
            #st.subheader("Discrete Probaility")
            gs_URL = st.session_state.gs_URL 
            googleSheetId = gs_URL.split("spreadsheets/d/")[1].split("/edit")[0]
            worksheetName = st.text_input("Sheet Name:","Discrete")
            URL = f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={worksheetName}'  
            if st.button('Refresh'):
                df = pd.read_csv(URL)
                df = df.dropna(axis=1, how="all")  
            df = pd.read_csv(URL)
            df = df.dropna(axis=1, how="all")
            with bottom[0]:
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
            x_axis = st.selectbox('X-Axis', options=numeric_columns, index=0)
            prob = st.selectbox('Probabilities', options=numeric_columns, index = 1)
            cat = 0
            if len(non_numeric_columns) >= 1: 
                cat = 1
                #cv = st.selectbox("Group", options=list(df[non_numeric_columns[0]].unique()))    
        if cat == 0:
            x = df[x_axis]
            p_x = df[prob]
            m =  sum(x*p_x)  
            sd = math.sqrt(sum((x-m)**2*p_x))
            data = pd.DataFrame({"Mean":m,"Std Dev":sd},index = [0])
            with top[2]:
                dph = ggplot(df) + geom_bar(aes(x=df[df.columns[0]],weight=df[df.columns[1]]),color="darkblue", fill="lightblue")
                st.pyplot(ggplot.draw(dph))
            with bottom[1]:
                st.write(data)
        if cat != 0:
            with bottom[1]:
                data = pd.DataFrame(columns = ['Type','Mean','Standard Deviation'])
                drow = 0
                for type in list(df[non_numeric_columns[0]].unique()):
                    df1 = df[df[non_numeric_columns[0]]==type]
                    x = df1[x_axis]
                    p_x = df1[prob]
                    data.loc[drow,'Type'] = type
                    m = sum(x*p_x)
                    data.loc[drow,'Mean'] =  m  
                    data.loc[drow,'Standard Deviation'] = math.sqrt(sum((x-m)**2*p_x))
                    drow = +1
                st.dataframe(data)
                    
            with top[2]:
                dph = ggplot(df) + geom_bar(aes(x=df[x_axis],weight=df[prob],fill=non_numeric_columns[0],color=non_numeric_columns[0]),position= "identity", alpha = .4)
                
                st.pyplot(ggplot.draw(dph))

            
            
        
    
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
            bph = ggplot(bdf) + geom_bar(aes(x=bdf["Hits"],weight=bdf["PDF"]),color="darkblue", fill="lightblue")
            st.pyplot(ggplot.draw(bph))

        
    if prob_choice == "Geometric Probability": 

        again = st.columns(2)    
        with again[0]:   
            st.subheader("Geometric Probability")
            gip, gih = st.text_input("Hit Probability:",.2,key ="1"),st.text_input("Tries:",4,key="2")
            gip = float(gip)
            gih = int(gih)
            giah = np.r_[0:gih+6]
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
            gph = ggplot(gdf) + geom_bar(aes(x=gdf["Hits"],weight=gdf["PDF"]),color="darkblue", fill="lightblue")
            st.pyplot(ggplot.draw(gph))


    if prob_choice == "Poisson Probability":      
        again = st.columns(2)     
        with again[0]:   
            st.subheader("Poisson Probability")
            peh, pah = st.text_input("Expected Hits:",2,key ="3"),st.text_input("Actual Hits:",4,key="4")
            peh = float(peh)
            pah = int(pah)
            paah = np.r_[0:pah+6]
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
            pph = ggplot(pdf) + geom_bar(aes(x=pdf["Hits"],weight=pdf["PDF"]),color="darkblue", fill="lightblue")
            st.pyplot(ggplot.draw(pph))
    
    
    
    
    