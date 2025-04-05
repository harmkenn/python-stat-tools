import streamlit as st
import plotly_express as px
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pingouin as pg

# Title
st.title("Quantitative Stats")

# Layout
top = st.columns((1, 1))
bottom = st.columns(1)

# Function to load and display data
def display_data(file_path, selected_sheet):
    try:
        df = pd.read_excel(file_path, sheet_name=selected_sheet)
        return df
    except FileNotFoundError:
        st.error("File not found. Please check the path and try again.")
    except (KeyError, ValueError):
        st.error(f"Sheet '{selected_sheet}' not found in the file.")
    return None

with top[0]:
    # Dropdown menu for sheet selection
    sheet_names = pd.read_excel(st.session_state.xlsx, sheet_name=None, nrows=0).keys()
    st.session_state.sheet = st.selectbox("Select sheet:", sheet_names, index=0)

    # Button to refresh data
    if st.button("Refresh Data"):
        df = display_data(st.session_state.xlsx, st.session_state.sheet)
    else:
        df = pd.read_excel(st.session_state.xlsx, sheet_name=st.session_state.sheet)

    if df is not None:
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns) + [None]
    else:
        st.error("Please upload a file to the application.")
        numeric_columns, non_numeric_columns = [], []

with top[1]:
    chart_choice = st.radio("Select Chart Type:", ["Histogram", "Boxplot & Dotplot", "QQplot", "Scatterplot"])

# Visualization logic
if df is not None:
    if chart_choice == "Histogram":
        with top[1]:
            x = st.selectbox('X-Axis', options=numeric_columns)
            cv = st.selectbox("Color", options=non_numeric_columns)
            bins = st.slider("Bins", min_value=1, max_value=20, value=7)

        fig = px.histogram(df, x=x, color=cv, marginal='rug', nbins=bins, facet_row=cv, template='simple_white') if cv else px.histogram(df, x=x, marginal='rug', nbins=bins)
        with top[1]:
            st.plotly_chart(fig, use_container_width=True)

    elif chart_choice == "Boxplot & Dotplot":
        with top[1]:
            x = st.selectbox('X-Axis', options=numeric_columns)
            cv = st.selectbox("Color", options=non_numeric_columns)

        fig = px.box(df, x=x, y=cv, points="all", color=cv) if cv else px.box(df, x=x, points="all")
        with top[1]:
            st.plotly_chart(fig, use_container_width=True)

    elif chart_choice == "QQplot":
        with top[1]:
            y = st.selectbox('Y-Axis', options=numeric_columns)
            cv = st.selectbox("Color", options=non_numeric_columns)

        ny = df[df[cv] == st.selectbox('Category', options=list(df[cv].unique()))][y] if cv else df[y]

        fig, ax = plt.subplots()
        ax = pg.qqplot(ny, dist='norm', confidence=.95)
        ax.set_xlabel('Theoretical Quantiles')
        ax.set_ylabel('Sample Quantiles')
        ax.set_title('QQ-Plot with Confidence Interval Bands')
        with top[1]:
            st.pyplot(fig, use_container_width=True)

    elif chart_choice == "Scatterplot":
        with top[1]:
            x = st.selectbox('X-Axis', options=numeric_columns)
            y = st.selectbox('Y-Axis', options=numeric_columns, index=1)
            cv = st.selectbox("Color", options=non_numeric_columns)

        fig = px.scatter(df, x=x, y=y, color=cv, trendline='ols') if cv else px.scatter(df, x=x, y=y, trendline='ols')
        with top[1]:
            st.plotly_chart(fig, use_container_width=True)

    # Display data tables
    with top[0]:
        st.write(df)

    with bottom[0]:
        st.write(df.describe().T)
        if cv:
            st.dataframe(df.groupby([cv]).describe())