import streamlit as st
import math
from scipy.stats import *
import pandas as pd
import numpy as np
from plotnine import *

def app():
    # title of the app
    st.markdown("Proportions")
    st.sidebar.subheader("Proportion Settings")
    prop_choice = st.sidebar.radio("",["One Proportion","Two Proportions"])
    
    if prop_choice == "One Proportion":
        c1,c2,c3 = st.columns(3)
        with c1:
            x = int(st.text_input("Hits",20))
            n = int(st.text_input("Tries",25))
        with c2:
            nullp = float(st.text_input("Null:",.7))
            alpha = float(st.text_input("Alpha",.05))
        with c3:
            st.markdown("Pick a test:")
            tail_choice = st.radio("",["Left Tail","Two Tails","Right Tail"])
    
        one = st.columns(1)
        with one[0]:
            p_hat = x/n
            tsd = math.sqrt(nullp*(1-nullp)/n)
            cise = math.sqrt(p_hat*(1-p_hat)/n)
            z = (p_hat - nullp)/tsd
            x = np.arange(-4,4,.1)
            y = norm.pdf(x)
            ndf = pd.DataFrame({"x":x,"y":y})
            normp = ggplot(ndf)  + coord_fixed(ratio = 4) 
            if tail_choice == "Left Tail":
                pv = norm.cdf(z)
                cz = norm.ppf(alpha)
                rcz = cz
                cl = 1 - 2*alpha
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "steelblue", xlim = (-4,z))
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "orange", xlim = (-4,cz))
            if tail_choice == "Two Tails":
                pv = 2*(1-norm.cdf(abs(z)))
                cz = abs(norm.ppf(alpha/2))
                rcz = "±" + str(abs(norm.ppf(alpha/2)))
                cl = 1 - alpha
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "steelblue", xlim = (-4,-1*abs(z)))
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "steelblue", xlim = (abs(z),4))
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "orange", xlim = (-4,-1*abs(cz)))
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "orange", xlim = (abs(cz),4))
            if tail_choice == "Right Tail":
                pv = 1 - norm.cdf(z)
                cz = -1 * norm.ppf(alpha)
                rcz = cz
                cl = 1 - 2*alpha
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "steelblue", xlim = (z,4))
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "orange", xlim = (cz,4))
            me = cz * cise
            rme = "±" + str(abs(me))
            data = pd.DataFrame({"p-Hat":p_hat,"z-Score":z,"p-Value":pv,"CV z*":rcz,"Test SD":tsd,"C-Level":cl,"CI SE":cise,"ME":rme},index = [0])  
            st.write(data)
            normp = normp + geom_segment(aes(x = z, y = 0, xend = z, yend = norm.pdf(z)),color="red")
            normp = normp + geom_line(aes(x=x,y=y)) + xlab('z') + ylab('')
            st.pyplot(ggplot.draw(normp))
            lower = p_hat - abs(me)
            upper = p_hat + abs(me) 
            st.write(str(100*cl) + "'%' confidence interval is (" + str(lower) +", "+str(upper)+")") 
        
    if prop_choice == "Two Proportions":
        c1,c2,c3 = st.columns(3)
        with c1:
            x1 = int(st.text_input("Hits 1",20))
            n1 = int(st.text_input("Tries 1",25))
            
        with c2:
            x2 = int(st.text_input("Hits 2",30))
            n2 = int(st.text_input("Tries 2",50))
        with c3:
            alpha = float(st.text_input("Alpha",.05))
            st.markdown("Pick a test:")
            tail_choice = st.radio("",["Left Tail","Two Tails","Right Tail"])
    
        one = st.columns(1)
        with one[0]:
            p_hat1 = x1/n1
            q_hat1 = 1 -p_hat1
            p_hat2 = x2/n2
            q_hat2 = 1 - p_hat2
            pp_hat = (x1+x2)/(n1+n2)
            dp_hat = p_hat1 - p_hat2
            pq_hat = 1-pp_hat
            tsd = math.sqrt(pp_hat*pq_hat*(1/n1+1/n2))
            cise = math.sqrt(p_hat1*q_hat1/n1+p_hat2*q_hat2/n2)
            z = (p_hat1 - p_hat2)/tsd
            
            x = np.arange(-4,4,.1)
            y = norm.pdf(x)
            ndf = pd.DataFrame({"x":x,"y":y})
            
            normp = ggplot(ndf) + coord_fixed(ratio = 4) 
            if tail_choice == "Left Tail":
                pv = norm.cdf(z)
                cz = norm.ppf(alpha)
                rcz = cz
                cl = 1 - 2*alpha
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "steelblue", xlim = (-4,z))
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "orange", xlim = (-4,cz))
            if tail_choice == "Two Tails":
                pv = 2*(1-norm.cdf(abs(z)))
                cz = abs(norm.ppf(alpha/2))
                rcz = "±" + str(abs(norm.ppf(alpha/2)))
                cl = 1 - alpha
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "steelblue", xlim = (-4,-1*abs(z)))
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "steelblue", xlim = (abs(z),4))
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "orange", xlim = (-4,-1*abs(cz)))
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "orange", xlim = (abs(cz),4))
            if tail_choice == "Right Tail":
                pv = 1 - norm.cdf(z)
                cz = -1 * norm.ppf(alpha)
                rcz = cz
                cl = 1 - 2*alpha
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "steelblue", xlim = (z,4))
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "orange", xlim = (cz,4))
            me = cz * cise
            rme = "±" + str(abs(me))
            data = pd.DataFrame({"p-Hat 1":p_hat1,"p-Hat 2":p_hat2,"Pooled p-Hat":pp_hat,"Diff p-Hat":dp_hat,"z-Score":z,"p-Value":pv,"CV z*":rcz,"Test SD":tsd,"C-Level":cl,"CI SE":cise,"ME":rme},index = [0])  
            st.write(data)
            normp = normp + geom_segment(aes(x = z, y = 0, xend = z, yend = norm.pdf(z)),color="red")
            normp = normp + geom_line(aes(x=x,y=y)) + xlab('z') + ylab('')
            st.pyplot(ggplot.draw(normp))
            lower = dp_hat - abs(me)
            upper = dp_hat + abs(me) 
            st.write(str(100*cl) + "'%' confidence interval is (" + str(lower) +", "+str(upper)+")") 
