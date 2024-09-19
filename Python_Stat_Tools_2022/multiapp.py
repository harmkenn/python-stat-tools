"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
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

        st.sidebar.title("Python Stat Tools v3.2")
        st.sidebar.subheader("by Ken Harmon")
        st.session_state.gs_URL = st.sidebar.text_input("Public Google Sheet URL:","https://docs.google.com/spreadsheets/d/1Fx7f6rM5Ce331F9ipsEMn-xRjUKYiR3R_v9IDBusUUY/edit#gid=0") 
               
        app = st.sidebar.radio(
            '',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()