import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import yaml
import streamlit as st

def login():
    """
    Handles user authentication using Streamlit and a configuration file.

    This function:
    - Loads authentication credentials and settings from a YAML config file.
    - Initializes the Streamlit-Authenticator object.
    - Prompts the user to log in via the Streamlit UI.
    - Manages authentication state (success, failure, or no input).
    - Displays appropriate messages and controls access based on login status.
    - Shows a logout button when authentication is successful.

    Raises:
        Displays Streamlit error messages if authentication fails or an exception occurs.
    """
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )

    try: 
        username = authenticator.login('main','Login')

    except Exception as e:
        st.error(e)

    if st.session_state.get("authentication_status") == True:   # login successful
        authenticator.logout('Logout', 'main')   # show logout button
    elif st.session_state.get("authentication_status") == False:
        st.error('Username/password is incorrect')
        st.stop()
    elif st.session_state.get("authentication_status") == None:
        st.warning('Please enter your username and password')
        st.stop()
