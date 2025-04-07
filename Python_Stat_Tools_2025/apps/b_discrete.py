import streamlit as st
import pandas as pd
from numpy import sqrt, arange
import plotly.express as px
from scipy.stats import binom, geom, poisson


# ---------- Helper Functions ----------

def display_discrete_data(file_path, sheet):
    try:
        return pd.read_excel(file_path, sheet_name=sheet)
    except (FileNotFoundError, KeyError, ValueError):
        st.error("Could not load data. Check file path or sheet name.")
        return pd.DataFrame()

def plot_bar(df, x, y, facet_row=None):
    fig = px.bar(df, x=x, y=y, facet_row=facet_row, template='simple_white')
    st.plotly_chart(fig, use_container_width=True)

def show_summary(mean, variance):
    st.write(pd.DataFrame({"Mean": [mean], "Std Dev": [sqrt(variance)]}))

def probability_distribution(title, x_label, dist_func, param1, param2=None, max_x=20):
    st.subheader(title)
    with out1:
        x_vals = arange(max_x)
        pdf = dist_func.pmf(x_vals, param1) if param2 is None else dist_func.pmf(x_vals, param1, param2)
        cdf = dist_func.cdf(x_vals, param1) if param2 is None else dist_func.cdf(x_vals, param1, param2)

    with out2:
        df = pd.DataFrame({x_label: x_vals, "PDF": pdf, "CDF": cdf})
        plot_bar(df, x=x_label, y='PDF')

        st.write(df)
        mean, var = dist_func.stats(param1) if param2 is None else dist_func.stats(param1, param2)
        show_summary(mean, var)

# ---------- UI Choice ----------

col1, col2 = st.columns((1,3))

with col1:

    prob_choice = st.radio("Choose Probability Type", [
        "Discrete Probability", 
        "Binomial Probability", 
        "Geometric Probability", 
        "Poisson Probability"
    ])

# ---------- Discrete Probability ----------

if prob_choice == "Discrete Probability":

    with col1:
        sheet_names = pd.read_excel(st.session_state.xlsx, sheet_name=None, nrows=0).keys()
        selected_sheet = st.selectbox("Select sheet:", sheet_names, index=1)

        if st.button("Refresh Data"):
            st.session_state.df = display_discrete_data(st.session_state.xlsx, selected_sheet)

        df = st.session_state.get('df', pd.read_excel(st.session_state.xlsx, selected_sheet))
        st.dataframe(df)

    with col2:
        if all(col in df.columns for col in ['X', 'Prob(X)', 'Type']):
            df['Mean'] = df['X'] * df['Prob(X)']
            mean_df = df.groupby('Type')['Mean'].sum().reset_index()

            df = pd.merge(df, mean_df, on='Type', suffixes=('', '_group'))
            df['SD'] = (df['X'] - df['Mean_group'])**2 * df['Prob(X)']
            std_df = df.groupby('Type')['SD'].sum().apply(sqrt)

            summary = pd.concat([mean_df.set_index('Type'), std_df], axis=1)
            summary.columns = ['Mean', 'Std Dev']
            st.dataframe(summary)

        if all(col in df.columns for col in ['X', 'Prob(X)', 'Type']):
            plot_bar(df, x='X', y='Prob(X)', facet_row='Type')

# ---------- Binomial Probability ----------

elif prob_choice == "Binomial Probability":
    prob = float(st.text_input("Hit Probability:", 0.2))
    trials = int(st.text_input("Tries:", 8))
    _ = st.text_input("Hits (not used):", 0)
    probability_distribution("Binomial Probability", "Hits", binom, trials, prob, trials + 1)

# ---------- Geometric Probability ----------

elif prob_choice == "Geometric Probability":
    prob = float(st.text_input("Hit Probability:", 0.2, key="geo_p"))
    tries = int(st.text_input("Tries:", 4, key="geo_h"))
    max_val = int(tries + 6 / prob)
    probability_distribution("Geometric Probability", "Tries", geom, prob, max_x=max_val)

# ---------- Poisson Probability ----------

elif prob_choice == "Poisson Probability":
    lam = float(st.text_input("Expected Hits (λ):", 2, key="pois_eh"))
    observed = int(st.text_input("Actual Hits:", 4, key="pois_ah"))
    max_val = int(observed + 2 * lam)
    probability_distribution("Poisson Probability", "Hits", poisson, lam, max_x=max_val)
