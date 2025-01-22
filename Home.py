import streamlit as st

# Fetch credentials from st.secrets
usernames = st.secrets['credentials']['usernames']

# Create a dictionary to map usernames to plain passwords
user_passwords = {}
for username, user_data in usernames.items():
    user_passwords[username] = user_data['password']

# Function to check login
def login(username, password):
    if username not in user_passwords:
        return False
    # Check if the entered password matches the stored plain password
    return password == user_passwords[username]

# Streamlit page logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False  # Track login status

# Handle login if user is not logged in
if not st.session_state['logged_in']:
    st.title("Login")
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type='password')

    # Submit button
    if st.button('Login'):
        if username_input and password_input:
            # Check the login credentials
            if login(username_input, password_input):
                st.session_state['logged_in'] = True  # Set login status to True
                st.success(f"Welcome, {usernames[username_input]['name']}!")
                st.rerun()  # Refresh the page to show the homepage
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter both username and password.")

# Show homepage if logged in
if st.session_state['logged_in']:
    st.title("Home Page")
    st.write("You are now logged in.")
