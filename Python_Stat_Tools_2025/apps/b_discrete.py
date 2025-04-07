import streamlit as st
import pandas as pd
from numpy import sqrt, arange
import plotly.express as px
from scipy.stats import binom, geom, poisson

# Sidebar selection
prob_choice = st.radio("Choose Probability Type", [
    "Discrete Probability", 
    "Binomial Probability", 
    "Geometric Probability", 
    "Poisson Probability"
])

# ---------- Helper Functions ----------

def display_discrete_data(file_path, sheet):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet)
        return df
    except FileNotFoundError:
        st.error("File not found. Please check the path and try again.")
    except (KeyError, ValueError):
        st.error(f"Sheet '{sheet}' not found in the file.")
    return pd.DataFrame()

def plot_bar(df, x, y, facet_row=None):
    fig = px.bar(df, x=x, y=y, facet_row=facet_row, template='simple_white')
    st.plotly_chart(fig, use_container_width=True)

def show_summary(mean, variance):
    summary = pd.DataFrame({
        "Mean": [mean],
        "Std Dev": [sqrt(variance)]
    })
    st.write(summary)

# ---------- Discrete Probability ----------

if prob_choice == "Discrete Probability":
    top = st.columns((1, 1, 2))

    with top[0]:
        sheet_names = pd.read_excel(st.session_state.xlsx, sheet_name=None, nrows=0).keys()
        st.session_state.sheet = st.selectbox("Select sheet:", sheet_names, index=1)

        if st.button("Refresh Data"):
            st.session_state.df = display_discrete_data(st.session_state.xlsx, st.session_state.sheet)

        df = pd.read_excel(st.session_state.xlsx, st.session_state.sheet)
        st.dataframe(df)

        try:
            numeric_columns = df.select_dtypes(include=['float', 'int']).columns.tolist()
            non_numeric_columns = df.select_dtypes(include='object').columns.tolist()
        except Exception as e:
            st.write("Please upload a valid file.")

    with top[1]:
        if 'X' in df.columns and 'Prob(X)' in df.columns and 'Type' in df.columns:
            df['Mean'] = df['X'] * df['Prob(X)']
            mean_df = df.groupby('Type')['Mean'].sum().reset_index()

            df = pd.merge(df, mean_df, on='Type', suffixes=('', '_grouped'))
            df['SD'] = (df['X'] - df['Mean_grouped'])**2 * df['Prob(X)']
            sd_df = df.groupby('Type')['SD'].sum().apply(sqrt)

            summary_df = pd.concat([mean_df.set_index('Type'), sd_df], axis=1)
            summary_df.columns = ['Mean', 'Std Dev']
            st.dataframe(summary_df)

    with top[2]:
        if 'X' in df.columns and 'Prob(X)' in df.columns and 'Type' in df.columns:
            plot_bar(df, x='X', y='Prob(X)', facet_row='Type')

# ---------- Binomial Probability ----------

elif prob_choice == "Binomial Probability":
    top = st.columns(2)

    with top[0]:
        st.subheader("Binomial Probability")
        bip = float(st.text_input("Hit Probability:", 0.2))
        bit = int(st.text_input("Tries:", 8))
        _ = st.text_input("Hits:", 0)  # Not used in logic

        x_vals = arange(bit + 1)
        pdf_vals = binom.pmf(x_vals, bit, bip)
        cdf_vals = binom.cdf(x_vals, bit, bip)

        df = pd.DataFrame({
            "Hits": x_vals,
            "PDF": pdf_vals,
            "CDF": cdf_vals
        })

    with top[1]:
        st.write(df)
        mean, var = binom.stats(bit, bip)
        show_summary(mean, var)

    with top[0]:
        plot_bar(df, x='Hits', y='PDF')

# ---------- Geometric Probability ----------

elif prob_choice == "Geometric Probability":
    cols = st.columns(2)

    with cols[0]:
        st.subheader("Geometric Probability")
        gip = float(st.text_input("Hit Probability:", 0.2, key="geo_p"))
        gih = int(st.text_input("Tries:", 4, key="geo_h"))

        max_val = int(gih + 6 / gip)
        x_vals = arange(max_val)
        pdf_vals = geom.pmf(x_vals, gip)
        cdf_vals = geom.cdf(x_vals, gip)

        df = pd.DataFrame({
            "Tries": x_vals,
            "PDF": pdf_vals,
            "CDF": cdf_vals
        })

    with cols[1]:
        st.write(df)
        mean, var = geom.stats(gip)
        show_summary(mean, var)

    with cols[0]:
        plot_bar(df, x='Tries', y='PDF')

# ---------- Poisson Probability ----------

elif prob_choice == "Poisson Probability":
    cols = st.columns(2)

    with cols[0]:
        st.subheader("Poisson Probability")
        peh = float(st.text_input("Expected Hits:", 2, key="pois_eh"))
        pah = int(st.text_input("Actual Hits:", 4, key="pois_ah"))

        max_val = int(pah + 2 * peh)
        x_vals = arange(max_val)
        pdf_vals = poisson.pmf(x_vals, peh)
        cdf_vals = poisson.cdf(x_vals, peh)

        df = pd.DataFrame({
            "Hits": x_vals,
            "PDF": pdf_vals,
            "CDF": cdf_vals
        })

    with cols[1]:
        st.write(df)
        mean, var = poisson.stats(peh)
        show_summary(mean, var)

    with cols[0]:
        plot_bar(df, x='Hits', y='PDF')
