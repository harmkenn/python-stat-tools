import streamlit as st
import pandas as pd
from plotnine import *
import scipy as sp
import numpy as np

def app():
    # title of the app
    
    anova_choice = st.sidebar.radio("ANOVA Choice",["Data","Statistics"])
    if anova_choice == "Data":
        c1,c2 = st.columns(2)
        with c1:
            st.subheader("ANOVA Data")
            gs_URL = st.text_input("Public Google Sheet URL:","https://docs.google.com/spreadsheets/d/1Fx7f6rM5Ce331F9ipsEMn-xRjUKYiR3R_v9IDBusUUY/edit#gid=0") 
            googleSheetId = gs_URL.split("spreadsheets/d/")[1].split("/edit")[0]
            worksheetName = st.text_input("Sheet Name:","Bivariate")
            URL = f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={worksheetName}'
            #@st.cache (ttl = 600)
            def upload_gs(x):
                out = pd.read_csv(x)
                return out

            df = upload_gs(URL)
            df = df.dropna(axis=1, how="all")
            st.dataframe(df.assign(hack='').set_index('hack')) 
            global numeric_columns
            global non_numeric_columns
            numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
            non_numeric_columns = list(df.select_dtypes(['object']).columns)
            st.sidebar.markdown("One Sample Data")
            quant = st.sidebar.selectbox('Quantitative Data', options=numeric_columns)
            cat = st.sidebar.selectbox('Categorical Data', options=non_numeric_columns)
        with c2:
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
            p = ggplot() + geom_boxplot(aes(x=sdf[cat],y=sdf[quant], fill = sdf[cat])) + coord_flip()
            st.pyplot(ggplot.draw(p))
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
            anovastats.loc['Withing (E)']=[wss,wdf,wms,None,None]
            st.dataframe(anovastats)
            
            alpha = float(st.text_input("Alpha:",.05))
            cv = sp.stats.f.ppf(1-alpha,bdf,wdf) 
            st.markdown("F Critical Value: "+ str(cv))
            maxF = max(aF,cv)
            x = np.arange(0,maxF*1.1,.03)
            Fy = sp.stats.f.pdf(x,bdf,wdf)
            Fdf = pd.DataFrame({"x":x,"Fy":Fy})
            Fplot = ggplot(Fdf) + coord_fixed(ratio = .5*maxF)
            Fdf["Right"] = np.where(Fdf["x"]>=aF,Fdf["Fy"],0)
            
            Fdf['alpha'] = np.where(Fdf["x"]>=cv,Fdf["Fy"],0)
            Fplot = Fplot + geom_col(aes(x=x,y="Right"), fill = "steelblue", size = .1, alpha = .4)
            Fplot = Fplot + geom_col(aes(x=x,y="alpha"), fill = "red", size = .1, alpha = .4)
            Fplot = Fplot + geom_segment(aes(x = aF, y = 0, xend = aF, yend = sp.stats.f.pdf(aF,bdf,wdf)),color="red")
            Fplot = Fplot + geom_line(aes(x=x,y=Fy))
            st.pyplot(ggplot.draw(Fplot))
    
    if anova_choice == "Statistics":
        c1,c2 = st.columns(2)
        with c1:
            st.subheader("ANOVA Statistics")
            gs_URL = st.text_input("Public Google Sheet URL:","https://docs.google.com/spreadsheets/d/1Fx7f6rM5Ce331F9ipsEMn-xRjUKYiR3R_v9IDBusUUY/edit#gid=0") 
            googleSheetId = gs_URL.split("spreadsheets/d/")[1].split("/edit")[0]
            worksheetName = st.text_input("Sheet Name:","ANOVA")
            URL = f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={worksheetName}'
            #@st.cache (ttl = 600)
            def upload_gs(x):
                out = pd.read_csv(x)
                return out

            sdfs = upload_gs(URL)
            sdfs = sdfs.dropna(axis=1, how="all").set_index('Group')
            st.dataframe(sdfs) 
            
        with c2:
            
            
            allmean = ((sdfs['count']*sdfs['mean']).sum())/(sdfs['count'].sum())
            meanmeans = sdfs['mean'].mean()
            sdfs['DMB']=sdfs['count']*(sdfs['mean']-allmean)**2
            sdfs['VW']=(sdfs['count']-1)*(sdfs['std'])**2
            st.markdown("Average of all items: " + str(allmean))
            st.markdown("Average of the means: " + str(meanmeans))
            st.dataframe(sdfs[['count','mean','std','DMB','VW']])
            
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
            anovastats.loc['Withing (E)']=[wss,wdf,wms,None,None]
            st.dataframe(anovastats)
            
            alpha = float(st.text_input("Alpha:",.05))
            cv = sp.stats.f.ppf(1-alpha,bdf,wdf) 
            st.markdown("F Critical Value: "+ str(cv))
            maxF = max(aF,cv)
            x = np.arange(0,maxF*1.1,.03)
            Fy = sp.stats.f.pdf(x,bdf,wdf)
            Fdf = pd.DataFrame({"x":x,"Fy":Fy})
            Fplot = ggplot(Fdf) + coord_fixed(ratio = .5*maxF)
            Fdf["Right"] = np.where(Fdf["x"]>=aF,Fdf["Fy"],0)
            
            Fdf['alpha'] = np.where(Fdf["x"]>=cv,Fdf["Fy"],0)
            Fplot = Fplot + geom_col(aes(x=x,y="Right"), fill = "steelblue", size = .1, alpha = .4)
            Fplot = Fplot + geom_col(aes(x=x,y="alpha"), fill = "red", size = .1, alpha = .4)
            Fplot = Fplot + geom_segment(aes(x = aF, y = 0, xend = aF, yend = sp.stats.f.pdf(aF,bdf,wdf)),color="red")
            Fplot = Fplot + geom_line(aes(x=x,y=Fy))
            st.pyplot(ggplot.draw(Fplot))        
    