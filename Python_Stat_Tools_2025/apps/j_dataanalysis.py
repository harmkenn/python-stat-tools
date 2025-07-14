import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Excel Data Visualizer")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("### Data Preview", df.head())

    # Auto-detect column types
    quantitative = df.select_dtypes(include=['number']).columns.tolist()
    categorical = df.select_dtypes(exclude=['number']).columns.tolist()

    st.sidebar.header("Column Type Overview")
    st.sidebar.write("**Quantitative:**", quantitative)
    st.sidebar.write("**Categorical:**", categorical)

    # User selection
    st.sidebar.header("Visualization Controls")
    x_col = st.sidebar.selectbox("X-axis", df.columns)
    y_col = st.sidebar.selectbox("Y-axis", df.columns, index=1 if len(df.columns) > 1 else 0)

    color_col = st.sidebar.selectbox("Color (Optional)", [None] + df.columns.tolist())

    filter_col = st.sidebar.selectbox("Filter by (Optional)", [None] + df.columns.tolist())
    if filter_col:
        filter_vals = df[filter_col].dropna().unique().tolist()
        selected_vals = st.sidebar.multiselect("Select values to include from " + filter_col, filter_vals, default=filter_vals)
        df = df[df[filter_col].isin(selected_vals)]

    # Visualization
    st.header("Generated Plot")
    try:
        if x_col in quantitative and y_col in quantitative:
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col)
        elif x_col in categorical and y_col in quantitative:
            fig = px.box(df, x=x_col, y=y_col, color=color_col)
        elif x_col in quantitative and y_col in categorical:
            fig = px.box(df, x=y_col, y=x_col, color=color_col, orientation='h')
        elif x_col in categorical and y_col in categorical:
            cross_tab = pd.crosstab(df[x_col], df[y_col])
            fig = go.Figure(data=[go.Heatmap(z=cross_tab.values, x=cross_tab.columns, y=cross_tab.index)])
        else:
            fig = px.histogram(df, x=x_col, color=color_col)

        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating plot: {e}")
