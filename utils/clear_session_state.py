import streamlit as st
from utils.jsonbin import del_first_count

def clear_session_state():
    """
    Clear leucocyte_count and diverse_count in the session_state powered by streamlit
    """ 
    del st.session_state.leucocyte_count
    del st.session_state.diverse_count
    if "leucocyte_count" in globals():
        del globals()["leucocygte_count"]
    if "diverse_count" in globals():
        del globals()["diverse_count"]

def clear_all(api_key, bin_id, username):
    """Delete the current count in streamlit's session_state and the first count saved in jsonbin"""
    clear_session_state()
    return del_first_count(api_key, bin_id, username)