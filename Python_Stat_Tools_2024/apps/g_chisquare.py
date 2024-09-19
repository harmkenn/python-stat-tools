
import streamlit as st
import pandas as pd
import scipy as sp
import numpy as np
import plotly_express as px


def app():
    # title of the app
    #st.markdown("Chi-Square")
    
    t_choice = st.radio("Chi-Square Test",["Chi-Square Test","Goodness of Fit"])
    
    if t_choice == "Chi-Square Test":
        c1,c2 = st.columns((1,1))
        with c1:
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
            st.session_state.sheet = st.selectbox("Select sheet:", sheet_names, index=3)
            
            # Button to refresh data
            if st.button("Refresh Data"):
                display_data(st.session_state.xlsx, st.session_state.sheet)               
            df = pd.read_excel(st.session_state.xlsx, st.session_state.sheet)
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
            chi = np.arange(0,maxchi*1.5,.1)
            chiy = sp.stats.chi2.pdf(chi,dof)
            chidf = pd.DataFrame({"chi":chi,"chiy":chiy})
            fig = px.line(chidf, x = 'chi', y = 'chiy', template= 'simple_white')
            chidf.loc[(chidf.chi <= tcs),'chiy'] = 0
            fig.add_trace(px.area(chidf, x = 'chi', y = 'chiy', template= 'simple_white').data[0])
            st.plotly_chart(fig, use_container_width=True)  
            
            
    if t_choice == "Goodness of Fit":
        c1,c2 = st.columns(2)
        with c1:
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
            st.session_state.sheet = st.selectbox("Select sheet:", sheet_names, index=4)
            # Button to refresh data
            if st.button("Refresh Data"):
                display_data(st.session_state.xlsx, st.session_state.sheet)               
            df = pd.read_excel(st.session_state.xlsx, st.session_state.sheet)
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
            maxchi = max(cv,tcs)
            chi = np.arange(0,maxchi*1.5,.1)
            chiy = sp.stats.chi2.pdf(chi,dof)
            chidf = pd.DataFrame({"chi":chi,"chiy":chiy})
            fig = px.line(chidf, x = 'chi', y = 'chiy', template= 'simple_white')
            chidf.loc[(chidf.chi <= tcs),'chiy'] = 0
            fig.add_trace(px.area(chidf, x = 'chi', y = 'chiy', template= 'simple_white').data[0])
            st.plotly_chart(fig, use_container_width=True) 
            