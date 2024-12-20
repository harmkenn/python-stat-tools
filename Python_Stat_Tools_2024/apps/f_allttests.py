from scipy.stats.morestats import shapiro
import streamlit as st
import math
import scipy
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statistics as stats
import plotly_express as px
import matplotlib.pyplot as plt
import pingouin as pg


def app():
    # title of the app

    t_choice = st.radio("T-Test Settings",["One Sample Data","One Sample Stats","Paired Sample Data","Two Sample Data","Two Sample Stats"])
    if t_choice == "One Sample Data":
        c1,c2,c3 = st.columns((2,1,2))
        with c1:
            
            #st.markdown("One Sample Data")
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
            
            quant = st.selectbox('Quantitative Data', options=numeric_columns)
            cat = st.selectbox('Categorical Data', options=non_numeric_columns)
            
            if cat != None:
                allcat = list(df[cat].unique())
                cat1 = st.selectbox('Category',options=allcat) 
                sdf = df[[quant,cat]]
                fsdf = sdf[sdf[cat]==cat1]
                st.markdown(f"Quantity: {quant}")
                st.markdown(f"Category: {cat}")   
                st.markdown(f"Variable: {cat1}")  
                
            if cat == None:
                fsdf = df[quant]
                st.markdown(f"Quantity: {quant}")
                st.markdown(f"Category: {cat}")  
            qstat = pd.DataFrame(fsdf.describe())
            st.write(qstat)
            fsdf=pd.DataFrame(fsdf)
        with c3:
            
            # Create a QQ-plot with confidence interval bands
            fig, ax = plt.subplots()
            ax = pg.qqplot(fsdf[quant], dist='norm', confidence=.95)

            # Add labels and title
            ax.set_xlabel('Theoretical Quantiles')
            ax.set_ylabel('Sample Quantiles')
            ax.set_title('QQ-Plot with Confidence Interval Bands')
            st.pyplot(fig, use_container_width=True)   

            ddd = shapiro(fsdf[quant])[1]
            st.write("Shapiro p-Value: " + str(ddd))
        
        st.markdown('''---''')
        d1,d2,d3 = st.columns((1,2,3))
        with d1:
            nh = float(st.text_input("Null Hypothesis:",67))
            alpha = float(st.text_input("Alpha:",0.05))
            tail_choice = st.radio("",["Left Tail","Two Tails","Right Tail"])
        with d2:
            n = qstat.iloc[0,0]
            df = n-1
            xbar = qstat.iloc[1,0]
            s = qstat.iloc[2,0]
            sem = s/math.sqrt(n)
            ts = (xbar - nh)/sem
            t = np.arange(-5,5,.01)
            ty = scipy.stats.t.pdf(t,df)
            tdf = pd.DataFrame({"t":t,"ty":ty})
            fig = px.line(tdf, x = 't', y = 'ty', template= 'simple_white') 

            
            if tail_choice == "Left Tail":
                pvalue = scipy.stats.t.cdf(ts,df)
                cv = scipy.stats.t.ppf(alpha,df)
                tdf.loc[(tdf.t >= ts),'ty'] = 0
                
                cl = 1 - 2*alpha
            if tail_choice == "Two Tails":
                rts = abs(ts)
                lts = -rts
                pvalue = 2*scipy.stats.t.cdf(lts,df)
                cv = scipy.stats.t.ppf(alpha/2,df)
                cv = abs(cv)
                tdf.loc[(tdf.t >= -abs(ts)) & (tdf.t <= abs(ts)),'ty'] = 0
                
                cl = 1-alpha
            if tail_choice == "Right Tail":
                pvalue = 1-scipy.stats.t.cdf(ts,df)
                cv = scipy.stats.t.ppf(1-alpha,df)
                tdf.loc[(tdf.t <= ts),'ty'] = 0
                
                cl=1-2*alpha
            me = cv*sem
            data = pd.DataFrame({"n":n,"df":df,"x-bar":xbar,"s":s,"sem":sem,"CV t*":cv,"ME":me,"t-Score":ts,"p-Value":pvalue},index = [0]).T 
            st.write(data) 
        with d3:
            fig.add_trace(px.area(tdf, x = 't', y = 'ty', template= 'simple_white').data[0])
            st.plotly_chart(fig, use_container_width=True)  
            lower = xbar - abs(me)
            upper = xbar + abs(me) 
            st.write(str(100*cl) + "'%' confidence interval is (" + str(lower) +", "+str(upper)+")") 

    if t_choice == "One Sample Stats":
        c1,c2 = st.columns((3,1))
        with c1:
            st.markdown("One Sample Stats")
            n = int(st.text_input("Sample Size (n):",12))
            
            xbar = float(st.text_input("Sample Mean (x-Bar):", 3.7))
            s = float(st.text_input("Sample Standard Deviation (s):", 1.2))
            
        st.markdown('''---''')
        d1,d2,d3 = st.columns((1,2,3))
        with d1:
            nh = float(st.text_input("Null Hypothesis:",4))
            alpha = float(st.text_input("Alpha:",0.05))
            tail_choice = st.radio("",["Left Tail","Two Tails","Right Tail"])
        with d2:
            
            df = n-1
            sem = s/math.sqrt(n)
            ts = (xbar - nh)/sem
            t = np.arange(-5,5,.01)
            ty = scipy.stats.t.pdf(t,df)
            tdf = pd.DataFrame({"t":t,"ty":ty})
            fig = px.line(tdf, x = 't', y = 'ty', template= 'simple_white') 
            
            if tail_choice == "Left Tail":
                pvalue = scipy.stats.t.cdf(ts,df)
                cv = scipy.stats.t.ppf(alpha,df)
                tdf.loc[(tdf.t >= ts),'ty'] = 0
                cl = 1 - 2*alpha
            if tail_choice == "Two Tails":
                rts = abs(ts)
                lts = -rts
                pvalue = 2*scipy.stats.t.cdf(lts,df)
                cv = scipy.stats.t.ppf(alpha/2,df)
                cv = abs(cv)
                tdf.loc[(tdf.t >= -abs(ts)) & (tdf.t <= abs(ts)),'ty'] = 0
                cl = 1-alpha
            if tail_choice == "Right Tail":
                pvalue = 1-scipy.stats.t.cdf(ts,df)
                cv = scipy.stats.t.ppf(1-alpha,df)
                tdf.loc[(tdf.t <= ts),'ty'] = 0
                cl=1-2*alpha
            me = cv*sem
            data = pd.DataFrame({"n":n,"df":df,"x-bar":xbar,"s":s,"sem":sem,"CV t*":cv,"ME":me,"t-Score":ts,"p-Value":pvalue},index = [0]).T 
            st.write(data) 
        with d3:
            fig.add_trace(px.area(tdf, x = 't', y = 'ty', template= 'simple_white').data[0])
            st.plotly_chart(fig, use_container_width=True) 
            
            lower = xbar - abs(me)
            upper = xbar + abs(me) 
            st.write(str(100*cl) + "'%' confidence interval is (" + str(lower) +", "+str(upper)+")")  
   
    if t_choice == "Paired Sample Data":
        c1,c2,c3 = st.columns((2,1,1))
        with c1:
            #st.markdown("Paired Sample Data")
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
            st.session_state.sheet = st.selectbox("Select sheet:", sheet_names, index=2)

            # Button to refresh data
            if st.button("Refresh Data"):
                display_data(st.session_state.xlsx, st.session_state.sheet)               
            df = pd.read_excel(st.session_state.xlsx, st.session_state.sheet)
            numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
            non_numeric_columns = list(df.select_dtypes(['object']).columns)
            non_numeric_columns.append(None)
            non_numeric_columns.reverse()
        with c2:    
            qb = st.selectbox('Before Data', options=numeric_columns)
            qa = st.selectbox('After Data', options=numeric_columns,index = 1)
            cat = st.selectbox('Categorical Data', options=non_numeric_columns)
        with c1:
            df['After-Before'] = df[qa]-df[qb]
            quant = 'After-Before'
            st.dataframe(df) 
        with c2:
            if cat != None:
                allcat = list(df[cat].unique())
                cat1 = st.selectbox('Category',options=allcat) 
                sdf = df[[quant,cat]]
                fsdf = sdf[sdf[cat]==cat1]
                st.markdown(f"Quantity: {quant}")
                st.markdown(f"Category: {cat}")   
                st.markdown(f"Variable: {cat1}")  
                
            if cat == None:
                fsdf = df[quant]
                st.markdown(f"Quantity: {quant}")
                st.markdown(f"Category: {cat}")  
            st.write(pd.DataFrame(fsdf.describe()))
            fsdf=pd.DataFrame(fsdf)
        with c3:
            # Create a QQ-plot with confidence interval bands
            fig, ax = plt.subplots()
            ax = pg.qqplot(fsdf[quant], dist='norm', confidence=.95)

            # Add labels and title
            ax.set_xlabel('Theoretical Quantiles')
            ax.set_ylabel('Sample Quantiles')
            ax.set_title('QQ-Plot with Confidence Interval Bands')
            st.pyplot(fig, use_container_width=True) 
             
            ddd = shapiro(fsdf[quant])[1]
            st.write("Shapiro p-Value: " + str(ddd))
        
        
        st.markdown('''---''')
        d1,d2,d3 = st.columns((1,2,3))
        with d1:
            nh = float(st.text_input("Null Hypothesis:",-2))
            alpha = float(st.text_input("Alpha:",0.05))
            tail_choice = st.radio("",["Left Tail","Two Tails","Right Tail"])
        with d2:
            n = len(fsdf)
            df = n-1
            xbar = stats.mean(fsdf[quant])
            s = stats.stdev(fsdf[quant])
            sem = s/math.sqrt(n)
            ts = (xbar - nh)/sem
            t = np.arange(-5,5,.01)
            ty = scipy.stats.t.pdf(t,df)
            tdf = pd.DataFrame({"t":t,"ty":ty})
            fig = px.line(tdf, x = 't', y = 'ty', template= 'simple_white') 
            
            if tail_choice == "Left Tail":
                pvalue = scipy.stats.t.cdf(ts,df)
                cv = scipy.stats.t.ppf(alpha,df)
                tdf.loc[(tdf.t >= ts),'ty'] = 0
                cl = 1 - 2*alpha
            if tail_choice == "Two Tails":
                rts = abs(ts)
                lts = -rts
                pvalue = 2*scipy.stats.t.cdf(lts,df)
                cv = scipy.stats.t.ppf(alpha/2,df)
                cv = abs(cv)
                tdf.loc[(tdf.t >= -abs(ts)) & (tdf.t <= abs(ts)),'ty'] = 0
                cl = 1-alpha
            if tail_choice == "Right Tail":
                pvalue = 1-scipy.stats.t.cdf(ts,df)
                cv = scipy.stats.t.ppf(1-alpha,df)
                tdf.loc[(tdf.t <= ts),'ty'] = 0
                cl=1-2*alpha
            me = cv*sem
            data = pd.DataFrame({"n":n,"df":df,"x-bar":xbar,"s":s,"sem":sem,"CV t*":cv,"ME":me,"t-Score":ts,"p-Value":pvalue},index = [0]).T 
            st.write(data) 
        with d3:
            fig.add_trace(px.area(tdf, x = 't', y = 'ty', template= 'simple_white').data[0])
            st.plotly_chart(fig, use_container_width=True)  
            lower = xbar - abs(me)
            upper = xbar + abs(me) 
            st.write(str(100*cl) + "'%' confidence interval is (" + str(lower) +", "+str(upper)+")") 
            
    if t_choice == "Two Sample Data":
        c1,c2,c3 = st.columns((1,1,1))
        with c1:
            #st.markdown("Two Sample Data")
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
            #st.dataframe(df.assign(hack='').set_index('hack')) 
            #global numeric_columns
            #global non_numeric_columns
            numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
            non_numeric_columns = list(df.select_dtypes(['object']).columns)
        with c2:    
            quant = st.selectbox('Common Variable', options=numeric_columns)
            cat = st.selectbox('Category', options=non_numeric_columns)
            allcat = list(df[cat].unique())
            g1 = st.selectbox('Group 1',options=allcat) 
            g2 = st.selectbox('Group 2',options=allcat, index = 1) 
        with c1:
            st.dataframe(df.assign(hack='').set_index('hack')) 
        if g1 == g2:
            with c2:
                st.warning('Select different Groups')
        if g1 != g2:
            with c2:
                sdf = df[[cat,quant]]
                groups = [g1,g2]
                fsdf = sdf[sdf[cat].isin(groups)]
                st.markdown(f"Quantity: {quant}")
                st.markdown(f"Category: {cat}")   
                st.markdown(f"Group 1: {g1}")  
                st.markdown(f"Group 1: {g2}")
                st.dataframe(fsdf.groupby(cat).describe().T)
                
            with c3:
                gp1 = fsdf[fsdf[cat]==g1][quant]
                # Create a QQ-plot with confidence interval bands
                fig, ax = plt.subplots()
                ax = pg.qqplot(gp1, dist='norm', confidence=.95)

                # Add labels and title
                ax.set_xlabel('Theoretical Quantiles')
                ax.set_ylabel('Sample Quantiles')
                ax.set_title('QQ-Plot with Confidence Interval Bands')
                st.pyplot(fig, use_container_width=True) 
                
                shap1 = scipy.stats.shapiro(gp1)
                st.write("Shapiro p-Value: " + str(shap1[1]))
                
            
                gp2 = fsdf[fsdf[cat]==g2][quant]
                # Create a QQ-plot with confidence interval bands
                fig, ax = plt.subplots()
                ax = pg.qqplot(gp2, dist='norm', confidence=.95)

                # Add labels and title
                ax.set_xlabel('Theoretical Quantiles')
                ax.set_ylabel('Sample Quantiles')
                ax.set_title('QQ-Plot with Confidence Interval Bands')
                st.pyplot(fig, use_container_width=True) 
                shap2 = scipy.stats.shapiro(gp2)
                st.write("Shapiro p-Value: " + str(shap2[1]))
            
            
            st.markdown('''---''')
            d1,d2,d3 = st.columns((1,1,2))
            with d1:
                nh = float(st.text_input("Null Hypothesis:",0))
                alpha = float(st.text_input("Alpha:",0.05))
                tail_choice = st.radio("",["Left Tail","Two Tails","Right Tail"])
                ev = st.checkbox("Equal Variances")
                
            with d2:
                st.write(cat+": "+g1+"-"+g2+ " "+ quant)

                sfsdf = pd.DataFrame(fsdf.groupby(cat).describe().T)
                
                n1 = sfsdf[g1].iloc[0]
                n2 = sfsdf[g2].iloc[0]
                sd1 = sfsdf[g1].iloc[2]
                sd2 = sfsdf[g2].iloc[2]
                
                se1 = sd1/math.sqrt(n1)
                se2 = sd2/math.sqrt(n2)
                sem = math.sqrt(se1**2+se2**2)
                xbard = sfsdf[g1].iloc[1]-sfsdf[g2].iloc[1]
                if ev:
                    df = n1+n2-2
                else:
                    df = sem**4/(sd1**4/(n1**2*(n1-1))+sd2**4/(n2**2*(n2-1)))
                ts = (xbard-nh)/sem
                
                #st.write(ts,df,sem)
                t = np.arange(-5,5,.01)
                ty = scipy.stats.t.pdf(t,df)
                tdf = pd.DataFrame({"t":t,"ty":ty})
                fig = px.line(tdf, x = 't', y = 'ty', template= 'simple_white') 
                
                if tail_choice == "Left Tail":
                    pvalue = scipy.stats.t.cdf(ts,df)
                    cv = scipy.stats.t.ppf(alpha,df)
                    tdf.loc[(tdf.t >= ts),'ty'] = 0
                    cl = 1 - 2*alpha
                if tail_choice == "Two Tails":
                    rts = abs(ts)
                    lts = -rts
                    pvalue = 2*scipy.stats.t.cdf(lts,df)
                    cv = scipy.stats.t.ppf(alpha/2,df)
                    cv = abs(cv)
                    tdf.loc[(tdf.t >= -abs(ts)) & (tdf.t <= abs(ts)),'ty'] = 0
                    cl = 1-alpha
                if tail_choice == "Right Tail":
                    pvalue = 1-scipy.stats.t.cdf(ts,df)
                    cv = scipy.stats.t.ppf(1-alpha,df)
                    tdf.loc[(tdf.t <= ts),'ty'] = 0
                    cl=1-2*alpha
                me = cv*sem
                data = pd.DataFrame({"df":df,"x-bar-d":xbard,"sem":sem,"CV t*":cv,"ME":abs(me),"t-Score":ts,"p-Value":pvalue},index = [0]).T 
                st.write(data) 
            with d3:
                fig.add_trace(px.area(tdf, x = 't', y = 'ty', template= 'simple_white').data[0])
                st.plotly_chart(fig, use_container_width=True)  
                lower = xbard - abs(me)
                upper = xbard + abs(me) 
                st.write(str(100*cl) + "'%' confidence interval is (" + str(lower) +", "+str(upper)+")") 

      
            
    if t_choice == "Two Sample Stats":
        c1,c2 = st.columns((2,2))
        with c1:
            #st.markdown("Two Sample Stats")
            n1 = int(st.text_input("Sample 1 Size (n1):",12))
            xbar1 = float(st.text_input("Sample 1 Mean (x-Bar1):", 3.7))
            s1 = float(st.text_input("Sample 1 Standard Deviation (s1):", 1.2))           
 
        with c2:
            n2 = int(st.text_input("Sample 2 Size (n2):",13))
            xbar2 = float(st.text_input("Sample 2 Mean (x-Bar2):", 3.5))
            s2 = float(st.text_input("Sample 2 Standard Deviation (s2):", 1.0))   
            
        st.markdown('''---''')
        d1,d2,d3 = st.columns((1,1,2))
        with d1:
            nh = float(st.text_input("Null Hypothesis:",0))
            alpha = float(st.text_input("Alpha:",0.05))
            tail_choice = st.radio("",["Left Tail","Two Tails","Right Tail"])
            ev = st.checkbox("Equal Variances")
                
        with d2:
            st.write("Sample 1 - Sample 2")
            se1 = s1/math.sqrt(n1)
            se2 = s2/math.sqrt(n2)
            sem = math.sqrt(se1**2+se2**2)
            xbard = xbar1 - xbar2
            if ev:
                df = n1+n2-2
            else:
                df = sem**4/(s1**4/(n1**2*(n1-1))+s2**4/(n2**2*(n2-1)))
            ts = (xbard-nh)/sem
            
            #st.write(ts,df,sem)
            t = np.arange(-5,5,.01)
            ty = scipy.stats.t.pdf(t,df)
            tdf = pd.DataFrame({"t":t,"ty":ty})
            fig = px.line(tdf, x = 't', y = 'ty', template= 'simple_white')
            if tail_choice == "Left Tail":
                pvalue = scipy.stats.t.cdf(ts,df)
                cv = scipy.stats.t.ppf(alpha,df)
                tdf.loc[(tdf.t >= ts),'ty'] = 0
                cl = 1 - 2*alpha
            if tail_choice == "Two Tails":
                rts = abs(ts)
                lts = -rts
                pvalue = 2*scipy.stats.t.cdf(lts,df)
                cv = scipy.stats.t.ppf(alpha/2,df)
                cv = abs(cv)
                tdf.loc[(tdf.t >= -abs(ts)) & (tdf.t <= abs(ts)),'ty'] = 0
                cl = 1-alpha
            if tail_choice == "Right Tail":
                pvalue = 1-scipy.stats.t.cdf(ts,df)
                cv = scipy.stats.t.ppf(1-alpha,df)
                tdf.loc[(tdf.t <= ts),'ty'] = 0
                cl=1-2*alpha
            me = cv*sem
            data = pd.DataFrame({"df":df,"x-bar-d":xbard,"sem":sem,"CV t*":cv,"ME":abs(me),"t-Score":ts,"p-Value":pvalue},index = [0]).T 
            st.write(data) 
        with d3:
            fig.add_trace(px.area(tdf, x = 't', y = 'ty', template= 'simple_white').data[0])
            st.plotly_chart(fig, use_container_width=True)  
            lower = xbard - abs(me)
            upper = xbard + abs(me) 
            st.write(str(100*cl) + "'%' confidence interval is (" + str(lower) +", "+str(upper)+")")   
