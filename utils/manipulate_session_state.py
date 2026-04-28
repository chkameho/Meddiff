import streamlit as st
import copy


def transfer_category_values(count_time_1, count_time_2, category):
    """
    Copies all values of a given category from one session_state entry to another.

    Args:
        count_time_1 (str): Key of the target session_state entry (the one being updated).
        count_time_2 (str): Key of the source session_state entry (the one providing the values).
        category (str): The category whose values should be transferred.
    """
    st.session_state[count_time_1][category] = copy.deepcopy(
        st.session_state[count_time_2][category])


def transfer_count(count_time_1,count_time_2):
    """
    Copies predefined count categories from one session_state entry to another.

    Args:
        count_time_1 (str): Key of the target session_state entry (the one being updated).
        count_time_2 (str): Key of the source session_state entry (the one providing the values).
    """
    transfer_category_values(count_time_1, count_time_2, "leucocyte_count")
    transfer_category_values(count_time_1, count_time_2, "diverse_count")

    