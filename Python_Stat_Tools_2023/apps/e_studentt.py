import streamlit as st
import scipy
import pandas as pd
import numpy as np
import plotly_express as px

def app():
    # title of the app
    st.markdown("Student t Probability")
    st.sidebar.subheader("t Settings")
    t_choice = st.sidebar.radio("",["t to Probability","Probability to t"])
    
    if t_choice == "t to Probability":
        c2,c3,c4 = st.columns(3)
        tp = 0

        with c2:
            lt = float(st.text_input("Left t", -1))
        with c3:
            st.markdown("Shade:")
            ls = st.checkbox("Left")
            cs = st.checkbox("Center",1)
            rs = st.checkbox("Right")
        with c4:
            rt = float(st.text_input("Right t",1))
        
        g1,g2 = st.columns((1,3))
        with g1:
            df = int(st.text_input("Degrees of Freedom:",2))
    
        with g2:
            t = np.arange(-5,5,.01)
            ny = scipy.stats.norm.pdf(t)
            ty = scipy.stats.t.pdf(t,df)
            tdf = pd.DataFrame({"t":t,"ny":ny,"ty":ty})
           
            fig = px.line(tdf, x = 't', y = 'ny', template= 'simple_white')            
            fig.update_traces(line_color='grey', line_dash='dash')
            
            fig.add_trace(px.line(tdf, x = 't', y = 'ty', template= 'simple_white').data[0])
            tp = 1

            if ls == 0:
                tp = tp - scipy.stats.t.cdf(lt,df)
                tdf.loc[(tdf.t <= lt),'ty'] = 0
                
            if cs == 0:
                tp = tp - (scipy.stats.t.cdf(rt,df) - scipy.stats.t.cdf(lt,df))
                tdf.loc[(tdf.t >= lt) & (tdf.t <= rt),'ty'] = 0
                
            if rs == 0:
                tp = tp - (1 - scipy.stats.t.cdf(rt,df))
                tdf.loc[(tdf.t >= rt),'ty'] = 0
            
            fig.add_trace(px.area(tdf, x = 't', y = 'ty', template= 'simple_white').data[0])
            
            st.plotly_chart(fig, use_container_width=True)  
                
        with g1:
            st.markdown(f"Total Probability: {tp}")
            
    if t_choice == "Probability to t":
        c2,c3,c4 = st.columns(3)

        with c2:
            sp = float(st.text_input("Probability", 40))
            
        with c3:
            st.markdown("Shade:")
            shade = st.radio("Shade:",["Left","Center","Right"])
        
        g1,g2 = st.columns((1,3))
        with g1:
            df = int(st.text_input("Degrees of Freedom:",2))
        with g2:
            t = np.arange(-5,5,.01)
            ny = scipy.stats.norm.pdf(t)
            ty = scipy.stats.t.pdf(t,df)
            tdf = pd.DataFrame({"t":t,"ny":ny,"ty":ty})
            fig = px.line(tdf, x = 't', y = 'ny', template= 'simple_white')            
            fig.update_traces(line_color='grey', line_dash='dash')
            
            fig.add_trace(px.line(tdf, x = 't', y = 'ty', template= 'simple_white').data[0])


            if shade == "Left":
                tscore = scipy.stats.t.ppf(sp/100,df)
                lt = tscore
                rt = tscore
                tdf.loc[(tdf.t >= lt),'ty'] = 0

                
            if shade == "Center":
                tscore = scipy.stats.t.ppf(((100-sp)/2)/100,df)
                lt = tscore 
                rt = -tscore
                tdf.loc[(tdf.t <= lt) | (tdf.t >= rt),'ty'] = 0

                
            if shade == "Right":
                tscore = scipy.stats.t.ppf((100-sp)/100,df)
                lt = tscore
                rt = tscore
                tdf.loc[(tdf.t <= rt),'ty'] = 0
            
            fig.add_trace(px.area(tdf, x = 't', y = 'ty', template= 'simple_white').data[0])
            
            st.plotly_chart(fig, use_container_width=True)  

        with g1:
            st.markdown(f"t-Score: {tscore}")
            if shade == "Center":
                st.markdown(f"t-Score: {rt}")
