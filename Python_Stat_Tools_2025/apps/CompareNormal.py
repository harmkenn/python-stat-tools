import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

# --- Page Config ---
st.set_page_config(page_title="Normal Distribution Comparator", layout="wide")

st.title("Normal Distribution Comparator")

# --- Sidebar Inputs ---
st.sidebar.header("Distribution Parameters")

st.sidebar.subheader("Distribution A")
mean_a = st.sidebar.number_input("Mean A", value=0.0)
std_a = st.sidebar.number_input("Std Dev A", value=1.0, min_value=0.0001)

st.sidebar.subheader("Distribution B")
mean_b = st.sidebar.number_input("Mean B", value=1.0)
std_b = st.sidebar.number_input("Std Dev B", value=1.0, min_value=0.0001)

# --- Generate X Range ---
x = np.linspace(
    min(mean_a - 4*std_a, mean_b - 4*std_b),
    max(mean_a + 4*std_a, mean_b + 4*std_b),
    500
)

# --- Compute PDFs ---
pdf_a = norm.pdf(x, mean_a, std_a)
pdf_b = norm.pdf(x, mean_b, std_b)

# --- Plotly Figure ---
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x, y=pdf_a,
    mode="lines",
    name=f"A: μ={mean_a}, σ={std_a}",
    line=dict(color="#00FFFF", width=3),
    opacity=0.6
))

fig.add_trace(go.Scatter(
    x=x, y=pdf_b,
    mode="lines",
    name=f"B: μ={mean_b}, σ={std_b}",
    line=dict(color="#FF00AA", width=3),
    opacity=0.6
))

fig.update_layout(
    template="plotly_dark",
    title="Normal Distribution Comparison",
    xaxis_title="X",
    yaxis_title="Probability Density",
    legend=dict(x=0.01, y=0.99)
)

st.plotly_chart(fig, use_container_width=True)
