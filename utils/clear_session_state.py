import streamlit as st
from utils.jsonbin import del_first_count

def clear_session_state(count_times):
    """
    Clear leucocyte_count and diverse_count in the session_state powered by streamlit
    """ 
    del st.session_state[count_times]["leucocyte_count"]
    del st.session_state[count_times]["diverse_count"]
    if "leucocyte_count" in globals():
        del globals()[count_times]["leucocygte_count"]
    if "diverse_count" in globals():
        del globals()["diverse_count"]
