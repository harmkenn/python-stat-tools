import streamlit as st
from multiapp import MultiApp
from apps import a_quant, b_discrete, c_normal, d_proportions, e_studentt, f_allttests, g_chisquare, h_linearregression, i_anova # import your app modules here
st.set_page_config(layout="wide")
app = MultiApp()

# Add all your application here
app.add_app("Quantitative Stats", a_quant.app)
app.add_app("Discrete Probability", b_discrete.app)
app.add_app("Normal Probability", c_normal.app)
app.add_app("Proportions", d_proportions.app)
app.add_app("Student T", e_studentt.app)
app.add_app("All T-Tests", f_allttests.app)
app.add_app("Chi-Square", g_chisquare.app)
app.add_app("Linear Regression", h_linearregression.app)
app.add_app("ANOVA", i_anova.app)

# The main app
app.run()