import streamlit as st


def check_authentication():
    """Redirect to the login page if the user is not authenticated."""
    if 'logged_in' not in st.session_state:
        st.warning("You must be logged in to access this page.")
        st.stop()  # Stops further execution of the page
