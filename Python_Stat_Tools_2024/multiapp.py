"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st
import pandas as pd

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):

        st.sidebar.title("Python Stat Tools v2024.2")
        st.sidebar.subheader("by Ken Harmon")
        


        # Input box for file path
        
        st.session_state.xlsx = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")
        if st.session_state.xlsx is None: st.session_state.xlsx = r"Default.xlsx"
        #st.session_state.xlsx = st.sidebar.text_input("Enter the path to your .xlsx file:",r"PythonStatsData.xlsx")
        
        st.sidebar.download_button(label="Download Default Excel File", data=open("Python_Sts_Tools_2024/PythonStatsData.xlsx", "rb").read(), file_name="PythonStatsData.xlsx")

           
        app = st.sidebar.radio(
            '',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()