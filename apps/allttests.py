from scipy.stats.morestats import shapiro
import streamlit as st
import math
import scipy
import pandas as pd
import numpy as np
from plotnine import *
import pingouin as pg
import statistics as stats


def app():
    # title of the app
    t_choice = st.sidebar.radio("T-Test Settings",["One Sample Data","Paired Sample Data","Two Sample Data","One Sample Stats","Two Sample Stats"])
    
    if t_choice == "One Sample Data":
        c1,c2,c3 = st.columns((2,1,2))
        with c1:
            gs_URL = st.text_input("Public Google Sheet URL:","https://docs.google.com/spreadsheets/d/1Fx7f6rM5Ce331F9ipsEMn-xRjUKYiR3R_v9IDBusUUY/edit#gid=0") 
            googleSheetId = gs_URL.split("spreadsheets/d/")[1].split("/edit")[0]
            worksheetName = st.text_input("Sheet Name:","Sheet5")
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
            non_numeric_columns.append(None)
            non_numeric_columns.reverse()
            st.sidebar.subheader("One Sample Data")
            quant = st.sidebar.selectbox('Quantitative Data', options=numeric_columns)
            cat = st.sidebar.selectbox('Categorical Data', options=non_numeric_columns)
            
        with c2:
            if cat != None:
                allcat = list(df[cat].unique())
                cat1 = st.sidebar.selectbox('Category',options=allcat) 
                sdf = df[[quant,cat]]
                fsdf = sdf[sdf[cat]==cat1]
                st.markdown(f"Quantity: {quant}")
                st.markdown(f"Category: {cat}")   
                st.markdown(f"Variable: {cat1}")  
                st.dataframe(fsdf.describe())
            if cat == None:
                fsdf = df[quant]
                st.markdown(f"Quantity: {quant}")
                st.markdown(f"Category: {cat}")  
                st.write(pd.DataFrame(fsdf.describe()))
            fsdf=pd.DataFrame(fsdf)
        with c3:
            p = pg.qqplot(fsdf[quant], dist='norm')
            st.pyplot(ggplot.draw(p))
            ddd = shapiro(fsdf[quant])[1]
            st.write("Shapiro p-Value: " + str(ddd))
        
        st.markdown('''---''')
        d1,d2,d3 = st.columns((1,2,3))
        with d1:
            nh = float(st.text_input("Null Hypothesis:",160))
            alpha = float(st.text_input("Alpha:",0.05))
            tail_choice = st.radio("",["Left Tail","Two Tails","Right Tail"])
        with d2:
            n = len(fsdf)
            df = n-1
            xbar = stats.mean(fsdf[quant])
            s = stats.stdev(fsdf[quant])
            sem = s/math.sqrt(n)
            ts = (xbar - nh)/sem
            x = np.arange(-5,5,.1)
            ty = scipy.stats.t.pdf(x,df)
            tdf = pd.DataFrame({"x":x,"ty":ty})
            tplot = ggplot(tdf) + coord_fixed(ratio = 4)
            if tail_choice == "Left Tail":
                pvalue = scipy.stats.t.cdf(ts,df)
                cv = scipy.stats.t.ppf(alpha,df)
                tdf["Left"] = np.where(tdf["x"]<=ts,tdf["ty"],0)
                tplot = tplot + geom_col(aes(x=x,y="Left"), fill = "steelblue", size = .1, alpha = .4)
                cl = 1 - 2*alpha
            if tail_choice == "Two Tails":
                rts = abs(ts)
                lts = -rts
                pvalue = 2*scipy.stats.t.cdf(lts,df)
                cv = scipy.stats.t.ppf(alpha/2,df)
                cv = abs(cv)
                tdf["Center"] = np.where(np.logical_or(tdf["x"]>=rts,tdf["x"]<=lts),tdf["ty"],0)
                tplot = tplot + geom_col(aes(x=x,y="Center"), fill = "steelblue", size = .1, alpha = .4)
                cl = 1-alpha
            if tail_choice == "Right Tail":
                pvalue = 1-scipy.stats.t.cdf(ts,df)
                cv = scipy.stats.t.ppf(1-alpha,df)
                tdf["Right"] = np.where(tdf["x"]>=ts,tdf["ty"],0)
                tplot = tplot + geom_col(aes(x=x,y="Right"), fill = "steelblue", size = .1, alpha = .4)
                cl=1-2*alpha
            me = cv*sem
            data = pd.DataFrame({"n":n,"df":df,"x-bar":xbar,"s":s,"sem":sem,"c-Value":cv,"ME":me,"t-Score":ts,"p-Value":pvalue},index = [0]).T 
            st.write(data) 
        with d3:
            tplot = tplot + geom_segment(aes(x = ts, y = 0, xend = ts, yend = scipy.stats.t.pdf(ts,df)),color="red")
            tplot = tplot + geom_line(aes(x=x,y=ty))
            st.pyplot(ggplot.draw(tplot))
            lower = xbar - abs(me)
            upper = xbar + abs(me) 
            st.write(str(100*cl) + "'%' confidence interval is (" + str(lower) +", "+str(upper)+")") 
    
    if t_choice == "Paired Sample Data":
        c1,c2,c3 = st.columns((2,1,2))
        with c1:
            gs_URL = st.text_input("Public Google Sheet URL:","https://docs.google.com/spreadsheets/d/1Fx7f6rM5Ce331F9ipsEMn-xRjUKYiR3R_v9IDBusUUY/edit#gid=0") 
            googleSheetId = gs_URL.split("spreadsheets/d/")[1].split("/edit")[0]
            worksheetName = st.text_input("Sheet Name:","Sheet5")
            URL = f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={worksheetName}'
            #@st.cache (ttl = 600)
            def upload_gs(x):
                out = pd.read_csv(x)
                return out

            df = upload_gs(URL)
            df = df.dropna(axis=1, how="all")
            #st.dataframe(df.assign(hack='').set_index('hack')) 
            #global numeric_columns
            #global non_numeric_columns
            numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
            non_numeric_columns = list(df.select_dtypes(['object']).columns)
            non_numeric_columns.append(None)
            non_numeric_columns.reverse()
            st.sidebar.subheader("Paired Sample Data")
            qb = st.sidebar.selectbox('Before Data', options=numeric_columns)
            qa = st.sidebar.selectbox('After Data', options=numeric_columns)
            cat = st.sidebar.selectbox('Categorical Data', options=non_numeric_columns)
            df['After-Before'] = df[qa]-df[qb]
            quant = 'After-Before'
            st.dataframe(df.assign(hack='').set_index('hack')) 
        with c2:
            if cat != None:
                allcat = list(df[cat].unique())
                cat1 = st.sidebar.selectbox('Category',options=allcat) 
                sdf = df[[quant,cat]]
                fsdf = sdf[sdf[cat]==cat1]
                st.markdown(f"Quantity: {quant}")
                st.markdown(f"Category: {cat}")   
                st.markdown(f"Variable: {cat1}")  
                st.dataframe(fsdf.describe())
            if cat == None:
                fsdf = df[quant]
                st.markdown(f"Quantity: {quant}")
                st.markdown(f"Category: {cat}")  
                st.write(pd.DataFrame(fsdf.describe()))
            fsdf=pd.DataFrame(fsdf)
        with c3:
            p = pg.qqplot(fsdf[quant], dist='norm')
            st.pyplot(ggplot.draw(p))
            ddd = shapiro(fsdf[quant])[1]
            st.write("Shapiro p-Value: " + str(ddd))
        
        
        st.markdown('''---''')
        d1,d2,d3 = st.columns((1,2,3))
        with d1:
            nh = float(st.text_input("Null Hypothesis:",0))
            alpha = float(st.text_input("Alpha:",0.05))
            tail_choice = st.radio("",["Left Tail","Two Tails","Right Tail"])
        with d2:
            n = len(fsdf)
            df = n-1
            xbar = stats.mean(fsdf[quant])
            s = stats.stdev(fsdf[quant])
            sem = s/math.sqrt(n)
            ts = (xbar - nh)/sem
            x = np.arange(-5,5,.1)
            ty = scipy.stats.t.pdf(x,df)
            tdf = pd.DataFrame({"x":x,"ty":ty})
            tplot = ggplot(tdf) + coord_fixed(ratio = 4)
            if tail_choice == "Left Tail":
                pvalue = scipy.stats.t.cdf(ts,df)
                cv = scipy.stats.t.ppf(alpha,df)
                tdf["Left"] = np.where(tdf["x"]<=ts,tdf["ty"],0)
                tplot = tplot + geom_col(aes(x=x,y="Left"), fill = "steelblue", size = .1, alpha = .4)
                cl = 1 - 2*alpha
            if tail_choice == "Two Tails":
                rts = abs(ts)
                lts = -rts
                pvalue = 2*scipy.stats.t.cdf(lts,df)
                cv = scipy.stats.t.ppf(alpha/2,df)
                cv = abs(cv)
                tdf["Center"] = np.where(np.logical_or(tdf["x"]>=rts,tdf["x"]<=lts),tdf["ty"],0)
                tplot = tplot + geom_col(aes(x=x,y="Center"), fill = "steelblue", size = .1, alpha = .4)
                cl = 1-alpha
            if tail_choice == "Right Tail":
                pvalue = 1-scipy.stats.t.cdf(ts,df)
                cv = scipy.stats.t.ppf(1-alpha,df)
                tdf["Right"] = np.where(tdf["x"]>=ts,tdf["ty"],0)
                tplot = tplot + geom_col(aes(x=x,y="Right"), fill = "steelblue", size = .1, alpha = .4)
                cl=1-2*alpha
            me = cv*sem
            data = pd.DataFrame({"n":n,"df":df,"x-bar":xbar,"s":s,"sem":sem,"c-Value":cv,"ME":me,"t-Score":ts,"p-Value":pvalue},index = [0]).T 
            st.write(data) 
        with d3:
            tplot = tplot + geom_segment(aes(x = ts, y = 0, xend = ts, yend = scipy.stats.t.pdf(ts,df)),color="red")
            tplot = tplot + geom_line(aes(x=x,y=ty))
            st.pyplot(ggplot.draw(tplot))
            lower = xbar - abs(me)
            upper = xbar + abs(me) 
            st.write(str(100*cl) + "'%' confidence interval is (" + str(lower) +", "+str(upper)+")") 
            
    if t_choice == "Two Sample Data":
        c1,c2,c3,c4 = st.columns((2,2,1,1))
        with c1:
            gs_URL = st.text_input("Public Google Sheet URL:","https://docs.google.com/spreadsheets/d/1Fx7f6rM5Ce331F9ipsEMn-xRjUKYiR3R_v9IDBusUUY/edit#gid=0") 
            googleSheetId = gs_URL.split("spreadsheets/d/")[1].split("/edit")[0]
            worksheetName = st.text_input("Sheet Name:","Sheet7")
            URL = f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={worksheetName}'
            #@st.cache (ttl = 600)
            def upload_gs(x):
                out = pd.read_csv(x)
                return out

            df = upload_gs(URL)
            df = df.dropna(axis=1, how="all")
            #st.dataframe(df.assign(hack='').set_index('hack')) 
            #global numeric_columns
            #global non_numeric_columns
            numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
            non_numeric_columns = list(df.select_dtypes(['object']).columns)
            non_numeric_columns.append(None)
            non_numeric_columns.reverse()
            st.sidebar.subheader("Two Sample Data")
            q1 = st.sidebar.selectbox('Set 1 Data', options=numeric_columns)
            q2 = st.sidebar.selectbox('Set 2 Data', options=numeric_columns)
            cat = st.sidebar.selectbox('Categorical Data', options=non_numeric_columns)
            st.dataframe(df.assign(hack='').set_index('hack')) 
        if q1 == q2:
            with c2:
                st.warning('Make set 1 and set 2 different')
        if q1 != q2:
            with c2:
                
                if cat != None:
                    allcat = list(df[cat].unique())
                    cat1 = st.sidebar.selectbox('Category',options=allcat) 
                    sdf = df[[q1,q2,cat]]
                    fsdf = sdf[sdf[cat]==cat1]
                    st.markdown(f"Set 1: {q1}")
                    st.markdown(f"Set 2: {q2}")
                    st.markdown(f"Category: {cat}")   
                    st.markdown(f"Variable: {cat1}")  
                    st.dataframe(fsdf.describe())
                if cat == None:
                    fsdf = df[[q1,q2]]
                    st.markdown(f"Set 1: {q1}")
                    st.markdown(f"Set 2: {q2}")
                    st.markdown(f"Category: {cat}")  
                    st.write(pd.DataFrame(fsdf.describe()))
                fsdf=pd.DataFrame(fsdf)
            with c3:
                p = pg.qqplot(fsdf[q1], dist='norm')
                st.pyplot(ggplot.draw(p))
                shap1 = scipy.stats.shapiro(fsdf[q1].dropna(axis=0, how="all"))
                st.write("Shapiro p-Value: " + str(shap1[1]))
                
            with c4:
                p = pg.qqplot(fsdf[q2], dist='norm')
                st.pyplot(ggplot.draw(p))
                shap2 = scipy.stats.shapiro(fsdf[q2].dropna(axis=0, how="all"))
                st.write("Shapiro p-Value: " + str(shap2[1]))
            
            
            st.markdown('''---''')
            d1,d2,d3 = st.columns((1,1,2))
            with d1:
                nh = float(st.text_input("Null Hypothesis:",0))
                alpha = float(st.text_input("Alpha:",0.05))
                tail_choice = st.radio("",["Left Tail","Two Tails","Right Tail"])
                ev = st.checkbox("Equal Variances")
                
            with d2:
                st.write("set 1 - set 2")

                sfsdf = pd.DataFrame(fsdf.describe())
                n1 = sfsdf[q1].iloc[0]
                n2 = sfsdf[q2].iloc[0]
                sd1 = sfsdf[q1].iloc[2]
                sd2 = sfsdf[q2].iloc[2]
                
                se1 = sd1/math.sqrt(n1)
                se2 = sd2/math.sqrt(n2)
                sem = math.sqrt(se1**2+se2**2)
                xbard = sfsdf[q1].iloc[1]-sfsdf[q2].iloc[1]
                if ev:
                    df = n1+n2-2
                else:
                    df = sem**4/(sd1**4/(n1**2*(n1-1))+sd2**4/(n2**2*(n2-1)))
                ts = (xbard-nh)/sem
                
                #st.write(ts,df,sem)
                x = np.arange(-5,5,.1)
                ty = scipy.stats.t.pdf(x,df)
                tdf = pd.DataFrame({"x":x,"ty":ty})
                tplot = ggplot(tdf) + coord_fixed(ratio = 4)
                if tail_choice == "Left Tail":
                    pvalue = scipy.stats.t.cdf(ts,df)
                    cv = scipy.stats.t.ppf(alpha,df)
                    tdf["Left"] = np.where(tdf["x"]<=ts,tdf["ty"],0)
                    tplot = tplot + geom_col(aes(x=x,y="Left"), fill = "steelblue", size = .1, alpha = .4)
                    cl = 1 - 2*alpha
                if tail_choice == "Two Tails":
                    rts = abs(ts)
                    lts = -rts
                    pvalue = 2*scipy.stats.t.cdf(lts,df)
                    cv = scipy.stats.t.ppf(alpha/2,df)
                    cv = abs(cv)
                    tdf["Center"] = np.where(np.logical_or(tdf["x"]>=rts,tdf["x"]<=lts),tdf["ty"],0)
                    tplot = tplot + geom_col(aes(x=x,y="Center"), fill = "steelblue", size = .1, alpha = .4)
                    cl = 1-alpha
                if tail_choice == "Right Tail":
                    pvalue = 1-scipy.stats.t.cdf(ts,df)
                    cv = scipy.stats.t.ppf(1-alpha,df)
                    tdf["Right"] = np.where(tdf["x"]>=ts,tdf["ty"],0)
                    tplot = tplot + geom_col(aes(x=x,y="Right"), fill = "steelblue", size = .1, alpha = .4)
                    cl=1-2*alpha
                me = cv*sem
                data = pd.DataFrame({"df":df,"x-bar-d":xbard,"sem":sem,"c-Value":cv,"ME":abs(me),"t-Score":ts,"p-Value":pvalue},index = [0]).T 
                st.write(data) 
            with d3:
                tplot = tplot + geom_segment(aes(x = ts, y = 0, xend = ts, yend = scipy.stats.t.pdf(ts,df)),color="red")
                tplot = tplot + geom_line(aes(x=x,y=ty))
                st.pyplot(ggplot.draw(tplot))
                lower = xbard - abs(me)
                upper = xbard + abs(me) 
                st.write(str(100*cl) + "'%' confidence interval is (" + str(lower) +", "+str(upper)+")") 
                