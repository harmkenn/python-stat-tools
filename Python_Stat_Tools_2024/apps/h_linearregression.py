import streamlit as st
import pandas as pd
import scipy as sp
import numpy as np
import plotly_express as px
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pingouin as pg



def app():
    # title of the app
    #st.markdown("Linear Regression") 
    
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
        st.session_state.sheet = st.selectbox("Select sheet:", sheet_names, index=0)
        # Button to refresh data
        if st.button("Refresh Data"):
            display_data(st.session_state.xlsx, st.session_state.sheet)               
        df = pd.read_excel(st.session_state.xlsx, st.session_state.sheet)
        st.dataframe(df.assign(hack='').set_index('hack')) 
        global numeric_columns
        global non_numeric_columns
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        non_numeric_columns.append(None)
        non_numeric_columns.reverse()
    with c2:    
        xvar = st.selectbox('X-Axis', options=numeric_columns, index = 0)
        yvar = st.selectbox('Y-Axis', options=numeric_columns, index = 1)
        cat = st.selectbox('Category', options=non_numeric_columns)
        
        if cat != None:
            allcat = list(df[cat].unique())
            cat1 = st.selectbox('Variable',options=allcat)
            sdf = df[[xvar,yvar,cat]]
            fsdf = sdf[sdf[cat]==cat1]
        if cat == None:
            fsdf = sdf = df[[xvar,yvar]]
    
        if xvar == yvar:
            st.warning("Select different X-Axis and Y-Axis")
        if xvar != yvar:
            
            fsdfs = fsdf.describe()
            st.dataframe(fsdfs.iloc[0:3,:])
            slope, intercept, r, p, ses = sp.stats.linregress(fsdf[xvar],fsdf[yvar])
            fsdf['predy']=intercept+slope*fsdf[xvar]
            fsdf['resid']=fsdf[yvar]-fsdf['predy']
            fsdf['sqresid']=fsdf['resid']**2
            sr = np.sqrt(fsdf['sqresid'].sum()/(fsdf['sqresid'].count()-2))
            data = pd.DataFrame({"r":r,'R-Squared':r**2,'se (resid)':sr,'Intercept':intercept,'Slope':slope,'se (slope)':ses,'t (slope)':slope/ses,'p (slope)':p},index = [0]).T 
            st.write(data)
            
             
    st.markdown('''---''')
    d1,d2 = st.columns(2)
    with d1:
        lr_graph = st.selectbox('Graph',["Scatter Plot","Residual QQPlot"])
        if lr_graph == "Scatter Plot":
           fig = px.scatter(fsdf, x = xvar, y = yvar, trendline='ols') 
           st.plotly_chart(fig, use_container_width=True)   
            
        if lr_graph == "Residual QQPlot":
            fig, ax = plt.subplots()
            ax = pg.qqplot(fsdf['resid'], dist='norm', confidence=.95)       
            # Add labels and title
            ax.set_xlabel('Theoretical Quantiles')
            ax.set_ylabel('Sample Quantiles')
            ax.set_title('QQ-Plot with Confidence Interval Bands')
            st.pyplot(fig, use_container_width=True)   

            ddd = sp.stats.shapiro(fsdf['resid'])[1]
            st.write("Shapiro p-Value: " + str(ddd))            

    with d2:
        gx =  float(st.text_input("Given X:",0)) 
        if xvar != yvar:
            py = intercept + slope*gx
            st.markdown("Predicted y: "+str(py))  
            alpha = float(st.text_input("alpha",.05))
            cl = 1-alpha
            n = len(fsdf)
            meanx = np.mean(fsdf[xvar])
            sdx = np.std(fsdf[xvar])
            dof = n-2
            ctv = sp.stats.t.ppf(alpha/2,dof) 
            slower = slope + ctv*ses
            shigher = slope - ctv*ses
            st.markdown(str(100*cl)+"'%' confidnce interval for slope: ("+str(slower)+","+str(shigher)+")")
            seyhat = sr*np.sqrt(1+1/n+(gx-meanx)**2/((n-1)*sdx**2))
            pime = ctv*seyhat
            plower = py + pime
            phigher = py - pime         
            st.markdown(str(100*cl)+"'%' prediction interval for y when x = "+str(gx)+": ("+str(plower)+","+str(phigher)+")")
            semuhat = sr*np.sqrt(1/n+(gx-meanx)**2/((n-1)*sdx**2))
            cimy = ctv*semuhat
            clower = py + cimy
            chigher = py - cimy 
            st.markdown(str(100*cl)+"'%' confidence interval for mean y when x = "+str(gx)+": ("+str(clower)+","+str(chigher)+")")