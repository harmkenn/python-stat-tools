import streamlit as st
from multiapp import MultiApp
from apps import quant, discrete, normal # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Quantitative Stats", quant.app)
app.add_app("Discrete Probability", discrete.app)
app.add_app("Normal Probability", normal.app)

# The main app
app.run()