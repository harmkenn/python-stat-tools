from typing import ClassVar
import streamlit as st
import pandas as pd
import scipy as sp
import numpy as np
from plotnine import *

def app():
    # title of the app
    st.markdown("Chi-Square")
    
    t_choice = st.sidebar.radio("Chi-Square Test",["Chi-Square Test","Goodness of Fit"])
    
    if t_choice == "Chi-Square Test":
        c1,c2 = st.columns((1,1))
        with c1:
            gs_URL = st.session_state.gs_URL 
            googleSheetId = gs_URL.split("spreadsheets/d/")[1].split("/edit")[0]
            worksheetName = st.text_input("Sheet Name:","Chi")
            URL = f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={worksheetName}'
            if st.button('Refresh'):
                df = pd.read_csv(URL)
                df = df.dropna(axis=1, how="all")  
            df = pd.read_csv(URL)
            df = df.dropna(axis=1, how="all")
            df = df.set_index('Chi')
            obc = df.values
            tcs, p, dof, exc = sp.stats.chi2_contingency(obc)
            csp = (obc - exc)**2/exc 
            dfexc=pd.DataFrame(exc)
            dfexc.columns = df.columns
            dfexc.index = df.index
            dft = df
            dft['total'] = dft.sum(axis = 1)
            dft.loc['total']=dft.sum()
            st.markdown("Observed Data")
            st.dataframe(dft)
            st.markdown("Expected Counts")
            st.dataframe(dfexc)
            
            
        with c2:
              
            st.markdown("Chi-Square Parts") 
            dfcsp = pd.DataFrame(csp)
            dfcsp.columns = dfexc.columns
            dfcsp.index = dfexc.index
            st.dataframe(dfcsp)
            alpha = float(st.text_input("Alpha",.05))
            cv = sp.stats.chi2.ppf(1-alpha,dof)
            data = pd.DataFrame({"Chi-Square Test Statistic":tcs,"Critical Value":cv,"Degrees of Freedom":dof,"p-Value":p},index = [0]).T 
            st.write(data)
            maxchi = max(cv,tcs)
            x = np.arange(0,maxchi+2,.1)
            chiy = sp.stats.chi2.pdf(x,dof)
            chidf = pd.DataFrame({"x":x,"chiy":chiy})
            chiplot = ggplot(chidf) + coord_fixed(ratio = 2*maxchi)
            chidf["Right"] = np.where(chidf["x"]>=tcs,chidf["chiy"],0)
            chidf['alpha'] = np.where(chidf["x"]>=cv,chidf["chiy"],0)
            chiplot = chiplot + geom_col(aes(x=x,y="Right"), fill = "steelblue", size = .1, alpha = .4)
            chiplot = chiplot + geom_col(aes(x=x,y="alpha"), fill = "red", size = .1, alpha = .4)
            chiplot = chiplot + geom_segment(aes(x = tcs, y = 0, xend = tcs, yend = sp.stats.t.pdf(tcs,dof)),color="red")
            chiplot = chiplot + geom_line(aes(x=x,y=chiy))
            st.pyplot(ggplot.draw(chiplot))
            
    if t_choice == "Goodness of Fit":
        c1,c2 = st.columns(2)
        with c1:
            gs_URL = st.session_state.gs_URL 
            googleSheetId = gs_URL.split("spreadsheets/d/")[1].split("/edit")[0]
            worksheetName = st.text_input("Sheet Name:","GOF")
            URL = f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={worksheetName}'
            if st.button('Refresh'):
                df = pd.read_csv(URL)
                df = df.dropna(axis=1, how="all")  
            df = pd.read_csv(URL)
            df = df.dropna(axis=1, how="all")
            obs = df['Observed'].values
            obss = obs.sum()
            rat = df['Ratio'].values
            rats = rat.sum()
            exp = rat/rats*obss
            df['Expected'] = exp
            csp = (obs-exp)**2/exp
            df['Chi-Square'] = csp
            tcs = csp.sum()
            st.dataframe(df)
            dof = len(df)-1
            p = 1-sp.stats.chi2.cdf(tcs,dof)
        with c2:
             
            alpha = float(st.text_input("Alpha",.05))
            cv = sp.stats.chi2.ppf(1-alpha,dof)
            data = pd.DataFrame({"Chi-Square Test Statistic":tcs,"Critical Value":cv,"Degrees of Freedom":dof,"p-Value":p},index = [0]).T 
            st.write(data)
            x = np.arange(0,cv+2,.1)
            chiy = sp.stats.chi2.pdf(x,dof)
            chidf = pd.DataFrame({"x":x,"chiy":chiy})
            chiplot = ggplot(chidf) + coord_fixed(ratio = cv)
            chidf["Right"] = np.where(chidf["x"]>=tcs,chidf["chiy"],0)
            chidf['alpha'] = np.where(chidf["x"]>=cv,chidf["chiy"],0)
            chiplot = chiplot + geom_col(aes(x=x,y="Right"), fill = "steelblue", size = .1, alpha = .4)
            chiplot = chiplot + geom_col(aes(x=x,y="alpha"), fill = "red", size = .1, alpha = .4)
            chiplot = chiplot + geom_segment(aes(x = tcs, y = 0, xend = tcs, yend = sp.stats.t.pdf(tcs,dof)),color="red")
            chiplot = chiplot + geom_line(aes(x=x,y=chiy)) + xlab('chi') + ylab('')
            st.pyplot(ggplot.draw(chiplot))