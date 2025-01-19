import streamlit as st
from utils.print_info import print_user_info
from utils import auth_functions

auth_functions.check_authentication()

st.header('User Information')

# Check if 'user_info' exists in session state and print recursively
if 'user_info' in st.session_state:
    print_user_info(st.session_state.user_info)
else:
    st.write("No user information available.")

st.subheader("Delete Account")
password = st.text_input(label='Confirm your password', type='password')
if st.button(label='Delete Account', on_click=auth_functions.delete_account, args=[password]):
    st.success('Your account has been deleted successfully.')