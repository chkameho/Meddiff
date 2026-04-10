import streamlit as st
import copy
from utils.jsonbin import del_first_count


def clear_session_state():
    """
    Clear leucocyte_count and diverse_count in the session_state powered by streamlit""" 
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

def sum_of_leucocyte(): 
    """Sum up the cell count in session_state.leucocyte_count"""
    return sum(st.session_state["leucocyte_count"].values())

def one_row_col(list_of_input,variable):
    """
    
    Arg:
        list_of_input
        variable (int): 
    """
    for key_name in list_of_input:
        if st.button(key_name, use_container_width = True):
                if key_name not in ["Normoblast","D","C"]:
                    st.session_state.leucocyte_count[key_name] += variable
                else:
                    st.session_state.diverse_count[key_name] += variable

def add_or_sub_one(add_or_sub_count):

    if add_or_sub_count == "addieren":
        variable = +1
    elif add_or_sub_count == "subtrahieren":
        variable = -1
    else:
        raise TypeError("Input can either be 'addieren' or 'subtrahieren'") 
    
    return variable

def HemaDiff_tool(add_or_sub_count):
    """
    A digital tool for counting different types of leukocytes 
    (basophils, monocytes, blasts, eosinophils, lymphocytes, segmented and rod-like neutrophils, myelocytes, plasma cells, and metamyelocytes), 
    as well as normocytes, powered by Streamlit for web visualization. Additionally, it includes diverse cell types represented as A, B, C, and D.

    Args:
    add_or_sub_count (str): Can be either "addieren" or "subtrahieren".
    """ 
    
    count = sum_of_leucocyte()

    variable = add_or_sub_one(add_or_sub_count)

    col1, col2, col3, col4 = st.columns(4, gap="small")

    if count <= 99:
       with col1:
           one_row_col(['Basophil','Monozyt','Blast','A'], variable = variable)
       with col2: 
           one_row_col(['Eosinophil','Lymphozyt','Promyelozyt','B'], variable = variable)
       with col3: 
           one_row_col(['Normoblast','Segmentierte','Myelozyt','C'], variable = variable)
       with col4: 
           one_row_col(['Plasmazelle','Stabkernige','Metamyelozyt','D'], variable = variable)


def Zählung_Dictionary(): 
    Dict = copy.deepcopy(st.session_state.leucocyte_count)
    for cell in st.session_state.diverse_count:
        Dict[cell] = st.session_state.diverse_count[cell]
    return Dict

def session_state_initialisieren(): 
    """Initialize streamlit.session_state to add 'leucocyte_count' and 'diverse_count' into the """
    leucocyte_count_dict = {'Basophil': 0, 'Monozyt':0, 'Blast':0,'A':0,'Eosinophil':0,'Lymphozyt':0,'Promyelozyt':0,'B':0,'Segmentierte':0,'Myelozyt':0,'Plasmazelle':0,'Stabkernige':0,'Metamyelozyt':0}
    diverse_count_dict = {'Normoblast':0, 'C':0, 'D':0}
    if "leucocyte_count" not in st.session_state:
        st.session_state.leucocyte_count = leucocyte_count_dict
    if "diverse_count" not in st.session_state:
        st.session_state.diverse_count = diverse_count_dict