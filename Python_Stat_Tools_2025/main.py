import streamlit as st
import importlib.util
import os 

# Set the page layout to wide
st.set_page_config(layout="wide", page_title=f"Python Stat Tools 2025")
st.sidebar.title("Python Stat Tools v2025.3")
st.sidebar.subheader("by Ken Harmon")

st.session_state.xlsx = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")
if st.session_state.xlsx is None: st.session_state.xlsx = r"Python_Stat_Tools_2025/Default.xlsx"
#st.session_state.xlsx = st.sidebar.text_input("Enter the path to your .xlsx file:",r"PythonStatsData.xlsx")
st.sidebar.download_button(label="Download Default Excel File", data=open("Python_Stat_Tools_2025/PythonStatsData.xlsx", "rb").read(), file_name="PythonStatsData.xlsx")

# Dictionary that maps .py filenames to user-friendly names
sub_app_names = {
    'a_quant.py': 'Quantitative Stat Data',
    'b_discrete.py': 'Discrete Probabilities',
    'c_normal.py': 'Normal Probabilities',
    'd_proportions.py': 'Proportion Tests',
    'e_studentt.py': 'T Probability',
    'f_allttests.py': 'All T Tests', 
    'g_chisquare.py': 'Chi-Square Tests',
    'h_linearregression.py': 'Linear Regression',
    'i_anova.py': 'ANOVA Tests',
    'j_dataanalysis.py': 'Data Analysis'
}

# Get a list of .py files from the SubApps folder
sub_apps_folder = os.path.join(os.path.dirname(__file__), 'apps')
sub_apps = [f for f in os.listdir(sub_apps_folder) if f.endswith('.py')]

# Create radio buttons in the sidebar using the user-friendly names
selected_sub_app_name = st.sidebar.radio('', list(sub_app_names.values()))

# Get the corresponding .py filename from the selected name
selected_sub_app = [k for k, v in sub_app_names.items() if v == selected_sub_app_name][0]

# Import and run the selected sub-app
if selected_sub_app:
    spec = importlib.util.spec_from_file_location(selected_sub_app, os.path.join(sub_apps_folder, selected_sub_app))
    sub_app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sub_app_module)