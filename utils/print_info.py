import streamlit as st

def print_user_info(user_info, indent=0):
    for key, value in user_info.items():
        # Add indentation using HTML
        indent_space = '&nbsp;' * indent  # Non-breaking space for indentation
        if isinstance(value, dict):  # If the value is a dictionary, recursively call the function
            st.markdown(f"{indent_space}<strong>{key}:</strong>", unsafe_allow_html=True)
            print_user_info(value, indent + 8)  # Increase indentation for nested dictionaries
        elif isinstance(value, list):  # If the value is a list, iterate through the list
            st.markdown(f"{indent_space}<strong>{key}:</strong>", unsafe_allow_html=True)
            for item in value:
                if isinstance(item, dict):  # If an item in the list is a dictionary, recursively print it
                    print_user_info(item, indent + 8)
                else:  # Otherwise, print the item directly
                    st.markdown(f"{indent_space}    - {item}", unsafe_allow_html=True)
        else:  # If the value is neither a dictionary nor a list, print it directly
            st.markdown(f"{indent_space}<strong>{key}:</strong> {value}", unsafe_allow_html=True)