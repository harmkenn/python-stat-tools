import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

# --- Page Config ---
st.set_page_config(page_title="Normal Distribution Comparator", layout="wide")
st.title("Normal Distribution Comparator")

# --- Sidebar Inputs ---
st.header("Distribution Parameters")

# --- Distribution A ---
st.subheader("Distribution A")
colA1, colA2 = st.columns(2)
mean_a = colA1.number_input("Mean A", value=0.0)
std_a = colA2.number_input("Std Dev A", value=1.0, min_value=0.0001)

# --- Distribution B ---
st.subheader("Distribution B")
colB1, colB2 = st.columns(2)
mean_b = colB1.number_input("Mean B", value=1.0)
std_b = colB2.number_input("Std Dev B", value=1.0, min_value=0.0001)

# --- Generate X Range ---
x = np.linspace(
    min(mean_a - 4*std_a, mean_b - 4*std_b),
    max(mean_a + 4*std_a, mean_b + 4*std_b),
    500
)

# --- Compute PDFs ---
pdf_a = norm.pdf(x, mean_a, std_a)
pdf_b = norm.pdf(x, mean_b, std_b)

# --- Quartiles ---
def quartiles(mean, sd):
    q1 = norm.ppf(0.25, mean, sd)
    q2 = norm.ppf(0.50, mean, sd)
    q3 = norm.ppf(0.75, mean, sd)
    return q1, q2, q3

q1_a, q2_a, q3_a = quartiles(mean_a, std_a)
q1_b, q2_b, q3_b = quartiles(mean_b, std_b)

# --- Plotly Figure ---
fig = go.Figure()

# Distribution A curve
fig.add_trace(go.Scatter(
    x=x, y=pdf_a,
    mode="lines",
    name=f"A: μ={mean_a}, σ={std_a}",
    line=dict(color="#00FFFF", width=3),
    opacity=0.6
))

# Distribution B curve
fig.add_trace(go.Scatter(
    x=x, y=pdf_b,
    mode="lines",
    name=f"B: μ={mean_b}, σ={std_b}",
    line=dict(color="#FF00AA", width=3),
    opacity=0.6
))

# --- Quartile Lines ---
quartile_lines = [
    (q1_a, "#00FFFF", "A Q1"),
    (q2_a, "#00FFFF", "A Median"),
    (q3_a, "#00FFFF", "A Q3"),
    (q1_b, "#FF00AA", "B Q1"),
    (q2_b, "#FF00AA", "B Median"),
    (q3_b, "#FF00AA", "B Q3"),
]

for qx, color, label in quartile_lines:
    fig.add_trace(go.Scatter(
        x=[qx, qx],
        y=[0, max(pdf_a.max(), pdf_b.max())],
        mode="lines",
        line=dict(color=color, width=1, dash="dash"),
        name=label
    ))

fig.update_layout(
    template="plotly_dark",
    title="Normal Distribution Comparison with Quartiles",
    xaxis_title="X",
    yaxis_title="Probability Density",
    legend=dict(x=0.01, y=0.99)
)

st.plotly_chart(fig, use_container_width=True)
