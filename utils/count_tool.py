import streamlit as st
import copy


def session_state_initialisieren(): 
    """Initialize streamlit.session_state to add 'leucocyte_count' and 'diverse_count' into the """
    leucocyte_count_dict = {'Basophil': 0, 'Monozyt':0, 'Blast':0,'A':0,'Eosinophil':0,
                            'Lymphozyt':0,'Promyelozyt':0,'B':0,'Segmentierte':0,'Myelozyt':0,
                            'Plasmazelle':0,'Stabkernige':0,'Metamyelozyt':0}
    diverse_count_dict = {'Normoblast':0, 'C':0, 'D':0}

    if "leucocyte_count" not in st.session_state:
        st.session_state.leucocyte_count = leucocyte_count_dict
    if "diverse_count" not in st.session_state:
        st.session_state.diverse_count = diverse_count_dict

def sum_of_leucocyte(): 
    """Sum up the cell count in session_state.leucocyte_count
    Return (int): The sum of the session_state leucocyte_count powered by streamlit"""
    return sum(st.session_state["leucocyte_count"].values())

def add_or_sub_one(add_or_sub_count):
    """
    Convert addieren to +1 and subtrahieren to -1.
    Arg: 
        add_or_sub_count(str): The input is either 'addieren' or 'subtrahieren',
    Raise:
        ValueError if the input is not 'addieren' or 'subtrahieren'. 
    Return:
        variable(int): +1 or -1 
    """
    if add_or_sub_count == "addieren":
        variable = +1
    elif add_or_sub_count == "subtrahieren":
        variable = -1
    else:
        raise ValueError("Input can either be 'addieren' or 'subtrahieren'") 
    
    return variable

def one_column_col(list_of_input,variable):
    """
    Create a column of four keys.
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
           one_column_col(['Basophil','Monozyt','Blast','A'], variable = variable)
       with col2: 
           one_column_col(['Eosinophil','Lymphozyt','Promyelozyt','B'], variable = variable)
       with col3: 
           one_column_col(['Normoblast','Segmentierte','Myelozyt','C'], variable = variable)
       with col4: 
           one_column_col(['Plasmazelle','Stabkernige','Metamyelozyt','D'], variable = variable)


def Zählung_Dictionary():
    "Connect the key leucocyte_count with diverse_count inside the session_state" 
    Dict = copy.deepcopy(st.session_state.leucocyte_count)
    for cell in st.session_state.diverse_count:
        Dict[cell] = st.session_state.diverse_count[cell]
    return Dict

