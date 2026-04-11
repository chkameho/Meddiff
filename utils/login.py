import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import yaml
import streamlit as st

def login():
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

login()