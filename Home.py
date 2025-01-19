import streamlit as st
from utils import auth_functions

# List of allowed emails
ALLOWED_EMAILS = ['jkilian.main@outlook.de', 'philipp.matzke@t-online.de']

def main():
    if 'user_info' not in st.session_state:
        col1, col2, col3 = st.columns([1, 2, 1])

        # Authentication form layout
        do_you_have_an_account = col2.selectbox(label='Do you have an account?', options=('Yes', 'No', 'I forgot my password'))
        auth_form = col2.form(key='Authentication form', clear_on_submit=False)
        email = auth_form.text_input(label='Email')
        password = auth_form.text_input(label='Password', type='password') if do_you_have_an_account in {'Yes', 'No'} else auth_form.empty()
        auth_notification = col2.empty()

        # Sign In
        if do_you_have_an_account == 'Yes' and auth_form.form_submit_button(label='Sign In', use_container_width=True, type='primary'):
            with auth_notification, st.spinner('Signing in'):
                auth_functions.sign_in(email, password)

        # Create Account
        elif do_you_have_an_account == 'No' and auth_form.form_submit_button(label='Create Account', use_container_width=True, type='primary'):
            # Check if the email is allowed to create an account
            if email not in ALLOWED_EMAILS:
                auth_notification.warning('This email is not allowed to create an account.')
            else:
                with auth_notification, st.spinner('Creating account'):
                    auth_functions.create_account(email, password)

        # Password Reset
        elif do_you_have_an_account == 'I forgot my password' and auth_form.form_submit_button(label='Send Password Reset Email', use_container_width=True, type='primary'):
            with auth_notification, st.spinner('Sending password reset link'):
                auth_functions.reset_password(email)

        # Authentication success and warning messages
        if 'auth_success' in st.session_state:
            auth_notification.success(st.session_state.auth_success)
            del st.session_state.auth_success
        elif 'auth_warning' in st.session_state:
            auth_notification.warning(st.session_state.auth_warning)
            del st.session_state.auth_warning

    # -------------------------------------------------------------------------------------------------
    # Logged in --------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------
    else:
        # Sidebar customization for logout
        st.title("Home")
        st.header('Welcome to Project M')
        st.write('Home page content goes here.')
        with st.sidebar:
            if st.button(label="Sign Out", key="logout"):
                # Clear session state and rerun the app to reset the state
                st.session_state.clear()  # Clear session data
                st.experimental_rerun()  # Rerun the app to reset session state

        # Streamlit automatically handles rendering the selected page
        st.write("")  # Placeholder to ensure sidebar renders cleanly


if __name__ == "__main__":
    main()
