import streamlit as st
from multiapp import MultiApp
from apps import quant, discrete, normal, proportions, studentt, allttests, chisquare, linearregression, anova # import your app modules here
st.set_page_config(layout="wide")
app = MultiApp()

# Add all your application here
app.add_app("Quantitative Stats", quant.app)
app.add_app("Discrete Probability", discrete.app)
app.add_app("Normal Probability", normal.app)
app.add_app("Proportions", proportions.app)
app.add_app("Student's T", studentt.app)
app.add_app("All t-Tests", allttests.app)
app.add_app("Chi-Square", chisquare.app)
app.add_app("Linear Regression", linearregression.app)
app.add_app("ANOVA", anova.app)

    
    

# The main app
app.run()