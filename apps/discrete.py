import streamlit as st
import plotly_express as px
import pandas as pd
from plotnine import *
from plotly.tools import mpl_to_plotly as ggplotly
import numpy as np
import math
from scipy.stats import *


def app():
    columns = st.columns(4)
    with columns[0]:
        st.subheader("Discrete Probaility")
        gs_URL = st.text_input("Public Google Sheet URL:","https://docs.google.com/spreadsheets/d/1Fx7f6rM5Ce331F9ipsEMn-xRjUKYiR3R_v9IDBusUUY/edit#gid=0") 
        googleSheetId = gs_URL.split("spreadsheets/d/")[1].split("/edit")[0]
        worksheetName = st.text_input("Sheet Name:","Sheet3")
        URL = f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={worksheetName}'    
        df = pd.read_csv(URL)
        df = df.dropna(axis=1, how="any")
        x = df["X"]
        p_x = df["Prob(X)"]
        m =  sum(x*p_x)  
        sd = math.sqrt(sum((x-m)**2*p_x))
        data = pd.DataFrame({"Mean":m,"Std Dev":sd},index = [0])
    with columns[1]:
        st.write(df),st.write(data)
    with columns[0]:
        dph = ggplot(df) + geom_bar(aes(x=df["X"],weight=df["Prob(X)"]),color="darkblue", fill="lightblue")
        st.pyplot(ggplot.draw(dph))
    with columns[2]:
        st.subheader("Binomial Probability")
        bip, bit, bih = st.text_input("Hit Probability:",.5),st.text_input("Tries:",10),st.text_input("Hits:",4)
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
    with columns[3]:
        st.write(bdf)
        data = pd.DataFrame({"Mean":bm,"Std Dev":math.sqrt(bv)},index = [0])
        st.write(data)
    with columns[2]:
        bph = ggplot(bdf) + geom_bar(aes(x=bdf["Hits"],weight=bdf["PDF"]),color="darkblue", fill="lightblue")
        st.pyplot(ggplot.draw(bph))
        
        
    again = st.columns(4)    
    with again[0]:   
        st.subheader("Geometric Probability")
        gip, gih = st.text_input("Hit Probability:",.5,key ="1"),st.text_input("Hits:",4,key="2")
        gip = float(gip)
        gih = int(gih)
        giah = np.r_[0:gih+6]
        cdf = geom.cdf(giah,gip)
        pmf = geom.pmf(giah,gip)
        giah = pd.DataFrame(giah)
        cdf = pd.DataFrame(cdf)
        pmf = pd.DataFrame(pmf)
        gm,gv = geom.stats(gip)
        gdf = pd.concat([biah,pmf,cdf],axis=1)
        gdf.columns = ["Hits","PDF","CDF"]
    with again[1]:
        st.write(gdf)
        data = pd.DataFrame({"Mean":gm,"Std Dev":math.sqrt(gv)},index = [0])
        st.write(data)
    with again[0]:
        gph = ggplot(gdf) + geom_bar(aes(x=gdf["Hits"],weight=gdf["PDF"]),color="darkblue", fill="lightblue")
        st.pyplot(ggplot.draw(gph))
    
    with again[2]:   
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
    with again[3]:
        st.write(pdf)
        data = pd.DataFrame({"Mean":pm,"Std Dev":math.sqrt(pv)},index = [0])
        st.write(data)
    with again[2]:
        pph = ggplot(pdf) + geom_bar(aes(x=pdf["Hits"],weight=pdf["PDF"]),color="darkblue", fill="lightblue")
        st.pyplot(ggplot.draw(pph))
    
    
    
    
    