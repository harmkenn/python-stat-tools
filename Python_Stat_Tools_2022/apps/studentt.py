import streamlit as st
import math
import scipy
import pandas as pd
import numpy as np
from plotnine import *

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
            x = np.arange(-5,5,.1)
            ny = scipy.stats.norm.pdf(x)
            ty = scipy.stats.t.pdf(x,df)
            tdf = pd.DataFrame({"x":x,"ny":ny,"ty":ty})
            tdf["Left"] = np.where(tdf["x"]<=lt,tdf["ty"],0)
            tdf["Center"] = np.where(np.logical_and(tdf["x"]>=lt,tdf["x"]<=rt),tdf["ty"],0)
            tdf["Right"] = np.where(tdf["x"]>=rt,tdf["ty"],0)

            tplot = ggplot(tdf) + geom_line(aes(x=x,y=ny),linetype = "dashed", color = "orange") + coord_fixed(ratio = 4) 
            if ls:
                tp = tp + scipy.stats.t.cdf(lt,df)
                tplot = tplot + geom_col(aes(x=x,y="Left"), fill = "steelblue", size = .1, alpha = .4) 
            if cs:
                tp = tp + scipy.stats.t.cdf(rt,df) - scipy.stats.t.cdf(lt,df)
                tplot = tplot + geom_col(aes(x=x,y="Center"), fill = "steelblue", size = .1, alpha = .4)
            if rs:
                tp = tp + 1 - scipy.stats.t.cdf(rt,df)
                tplot = tplot + geom_col(aes(x=x,y="Right"), fill = "steelblue", size = .1, alpha = .4)
            tplot = tplot + geom_segment(aes(x = lt, y = 0, xend = lt, yend = scipy.stats.t.pdf(lt,df)),color="red")
            tplot = tplot + geom_segment(aes(x = rt, y = 0, xend = rt, yend = scipy.stats.t.pdf(rt,df)),color="red")
            tplot = tplot + geom_line(aes(x=x,y=ty)) + xlab('t') + ylab('')
            
            st.pyplot(ggplot.draw(tplot))
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
            x = np.arange(-5,5,.1)
            y = scipy.stats.t.pdf(x,df)
            tdf = pd.DataFrame({"x":x,"y":y})
            tplot = ggplot(tdf)  + coord_fixed(ratio = 4) 
            
            
            

            if shade == "Left":
                t = scipy.stats.t.ppf(sp/100,df)
                lt = t
                rt = t
                tdf["Left"] = np.where(tdf["x"]<=lt,tdf["y"],0)
                tplot = ggplot(tdf)  + coord_fixed(ratio = 4)
                tplot = tplot + geom_col(aes(x=x,y="Left"), fill = "steelblue", size = .1, alpha = .4) 
                
            if shade == "Center":
                t = scipy.stats.t.ppf(((100-sp)/2)/100,df)
                lt = t 
                rt = -t
                tdf["Center"] = np.where(np.logical_and(tdf["x"]>=lt,tdf["x"]<=rt),tdf["y"],0)
                tplot = ggplot(tdf)  + coord_fixed(ratio = 4)
                tplot = tplot + geom_col(aes(x=x,y="Center"), fill = "steelblue", size = .1, alpha = .4)
                
            if shade == "Right":
                t = scipy.stats.t.ppf((100-sp)/100,df)
                lt = t
                rt = t
                tdf["Right"] = np.where(tdf["x"]>=rt,tdf["y"],0)
                tplot = ggplot(tdf)  + coord_fixed(ratio = 4)
                tplot = tplot + geom_col(aes(x=x,y="Right"), fill = "steelblue", size = .1, alpha = .4)
                
            tplot = tplot + geom_segment(aes(x = lt, y = 0, xend = lt, yend = scipy.stats.t.pdf(lt,df)),color="red")
            tplot = tplot + geom_segment(aes(x = rt, y = 0, xend = rt, yend = scipy.stats.t.pdf(rt,df)),color="red")
            tplot = tplot + geom_line(aes(x=x,y=y)) + xlab('t') + ylab('')
            
            st.pyplot(ggplot.draw(tplot))
        with g1:
            st.markdown(f"t-Score: {t}")
            if shade == "Center":
                st.markdown(f"t-Score: {rt}")
