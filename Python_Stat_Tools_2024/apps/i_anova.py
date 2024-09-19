import streamlit as st
import plotly_express as px
import pandas as pd
import statsmodels.api as sm
import scipy as sp
import numpy as np

def app():
    # title of the app
    
    anova_choice = st.radio("",["Data","Statistics"])
    
    if anova_choice == "Data":
        c1,c2 = st.columns(2)
        with c1:
            #st.markdown('ANOVA') 
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
            
        with c2:
            st.markdown("One Sample Data")
            quant = st.selectbox('Quantitative Data', options=numeric_columns)
            cat = st.selectbox('Categorical Data', options=non_numeric_columns)
            sdf = df[[quant,cat]]
            sdfs = sdf.groupby(cat).describe()
            sdfs = sdfs[quant]
            allmean = sdf[quant].mean()
            meanmeans = sdfs['mean'].mean()
            sdfs['DMB']=sdfs['count']*(sdfs['mean']-allmean)**2
            sdfs['VW']=(sdfs['count']-1)*(sdfs['std'])**2
            st.markdown("Average of all " + quant + "s: " + str(allmean))
            st.markdown("Average of the " + cat +" Mean " + quant + "s: " + str(meanmeans))
            st.dataframe(sdfs[['count','mean','std','DMB','VW']])
            fig = px.box(df, x=quant, y=cat, points="all",color=cat)
            st.plotly_chart(fig, use_container_width=True)  
            
            
        st.markdown('''---''')
        d1,d2 = st.columns((5,1))
        with d1:
            anovastats = pd.DataFrame(columns=('Sum of Squares',"df","Mean Square","F",'P-Value'))
            bss = sdfs['DMB'].sum()
            bdf = len(sdfs)-1
            bms = bss/bdf
            wss = sdfs['VW'].sum()
            wdf = sdfs['count'].sum()-len(sdfs)
            wms = wss/wdf
            aF = bms/wms
            Fp = 1 - sp.stats.f.cdf(aF,bdf,wdf)
            anovastats.loc['Between (TR)']=[bss,bdf,bms,aF,Fp]
            anovastats.loc['Within (E)']=[wss,wdf,wms,None,None]
            st.dataframe(anovastats)
            
            alpha = float(st.text_input("Alpha:",.05))
            cv = sp.stats.f.ppf(1-alpha,bdf,wdf) 
            st.markdown("F Critical Value: "+ str(cv))
            maxF = max(aF,cv)
            F = np.arange(0,maxF*1.1,.01)
            
            Fy = sp.stats.f.pdf(F,bdf,wdf)
            Fdf = pd.DataFrame({"F":F,"Fy":Fy})
            
            fig = px.line(Fdf, x = 'F', y = 'Fy', template= 'simple_white')
            Fdf.loc[(Fdf.F <= aF),'Fy'] = 0
            fig.add_trace(px.area(Fdf, x = 'F', y = 'Fy', template= 'simple_white').data[0])
            st.plotly_chart(fig, use_container_width=True) 
            
            
    
    if anova_choice == "Statistics":
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
            st.session_state.sheet = st.selectbox("Select sheet:", sheet_names, index=5)
            # Button to refresh data
            if st.button("Refresh Data"):
                display_data(st.session_state.xlsx, st.session_state.sheet)               
            df = pd.read_excel(st.session_state.xlsx, st.session_state.sheet)
            
            sdfs =  df
        with c2:
            
            
            allmean = ((sdfs['count']*sdfs['mean']).sum())/(sdfs['count'].sum())
            meanmeans = sdfs['mean'].mean()
            sdfs['DMB']=sdfs['count']*(sdfs['mean']-allmean)**2
            sdfs['VW']=(sdfs['count']-1)*(sdfs['std'])**2
            st.markdown("Average of all items: " + str(allmean))
            st.markdown("Average of the means: " + str(meanmeans))
            st.dataframe(sdfs[['Group','count','mean','std','DMB','VW']])
            
            
            
        st.markdown('''---''')
        d1,d2 = st.columns((5,1))
        with d1:
            anovastats = pd.DataFrame(columns=('Sum of Squares',"df","Mean Square","F",'P-Value'))
            bss = sdfs['DMB'].sum()
            bdf = len(sdfs)-1
            bms = bss/bdf
            wss = sdfs['VW'].sum()
            wdf = sdfs['count'].sum()-len(sdfs)
            wms = wss/wdf
            aF = bms/wms
            Fp = 1 - sp.stats.f.cdf(aF,bdf,wdf)
            anovastats.loc['Between (TR)']=[bss,bdf,bms,aF,Fp]
            anovastats.loc['Within (E)']=[wss,wdf,wms,None,None]
            st.dataframe(anovastats)
            
            alpha = float(st.text_input("Alpha:",.05))
            cv = sp.stats.f.ppf(1-alpha,bdf,wdf) 
            st.markdown("F Critical Value: "+ str(cv))
            maxF = max(aF,cv)
            F = np.arange(0,maxF*1.1,maxF/1000)
            Fy = sp.stats.f.pdf(F,bdf,wdf)
            Fdf = pd.DataFrame({"F":F,"Fy":Fy})
            
            fig = px.line(Fdf, x = 'F', y = 'Fy', template= 'simple_white')
            Fdf.loc[(Fdf.F <= aF),'Fy'] = 0
            fig.add_trace(px.area(Fdf, x = 'F', y = 'Fy', template= 'simple_white').data[0])
            st.plotly_chart(fig, use_container_width=True) 
                
    