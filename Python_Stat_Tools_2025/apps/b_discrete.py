import streamlit as st
import plotly_express as px
import pandas as pd
from scipy.stats import binom, geom, poisson

def display_data(file_path, selected_sheet):
    try:
        df = pd.read_excel(file_path, sheet_name=selected_sheet)
    except FileNotFoundError:
        st.error("File not found. Please check the path and try again.")
    except (KeyError, ValueError):
        st.error(f"Sheet '{selected_sheet}' not found in the file.")
    return df

def calculate_discrete_probability(df):
    df['Mean'] = df['X'] * df['Prob(X)']
    m = df.groupby(['Type'])['Mean'].sum()
    df = pd.merge(df, m, on='Type', how='inner')
    df['SD'] = (df['X'] - df['Mean_y']) ** 2 * df['Prob(X)']
    n = df.groupby(['Type'])['SD'].sum() ** (1 / 2)
    mn = pd.concat([m, n], axis=1)
    return mn

def calculate_binomial_probability(hit_prob, tries, hits):
    biah = np.r_[0:tries + 1]
    cdf = binom.cdf(biah, tries, hit_prob)
    pmf = binom.pmf(biah, tries, hit_prob)
    bdf = pd.concat([biah, pmf, cdf], axis=1)
    bdf.columns = ["Hits", "PDF", "CDF"]
    return bdf

def calculate_geometric_probability(hit_prob, tries):
    giah = np.r_[0:tries + 6 / hit_prob]
    cdf = geom.cdf(giah, hit_prob)
    pmf = geom.pmf(giah, hit_prob)
    gdf = pd.concat([giah, pmf, cdf], axis=1)
    gdf.columns = ["Tries", "PDF", "CDF"]
    return gdf

def calculate_poisson_probability(expected_hits, actual_hits):
    paah = np.r_[0:actual_hits + expected_hits * 2]
    cdf = poisson.cdf(paah, expected_hits)
    pmf = poisson.pmf(paah, expected_hits)
    pdf = pd.concat([paah, pmf, cdf], axis=1)
    pdf.columns = ["Hits", "PDF", "CDF"]
    return pdf

def main():
    prob_choice = st.radio("", ["Discrete Probability", "Binomial Probability", "Geometric Probability", "Poisson Probability"])

    if prob_choice == "Discrete Probability":
        df = display_data(st.session_state.xlsx, st.session_state.sheet)
        mn = calculate_discrete_probability(df)
        st.dataframe(mn)
        fig = px.bar(df, x='X', y='Prob(X)', facet_row='Type', template='simple_white')
        st.plotly_chart(fig, use_container_width=True)

    elif prob_choice == "Binomial Probability":
        hit_prob = float(st.text_input("Hit Probability:", 0.2))
        tries = int(st.text_input("Tries:", 8))
        hits = int(st.text_input("Hits:", 0))
        bdf = calculate_binomial_probability(hit_prob, tries, hits)
        st.write(bdf)
        data = pd.DataFrame({"Mean": binom.stats(tries, hit_prob)[0], "Std Dev": math.sqrt(binom.stats(tries, hit_prob)[1])}, index=[0])
        st.write(data)
        fig = px.bar(bdf, x='Hits', y='PDF', template='simple_white')
        st.plotly_chart(fig, use_container_width=True)

    elif prob_choice == "Geometric Probability":
        hit_prob = float(st.text_input("Hit Probability:", 0.2, key="1"))
        tries = int(st.text_input("Tries