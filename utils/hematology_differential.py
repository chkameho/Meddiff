import streamlit as st
import copy

class HematologyDifferential:
    """
    Streamlit-based tool for performing a hematology differential cell count.

    This class manages interactive counting of different leukocyte subtypes
    and additional (diverse) cell types using Streamlit session state.

    It provides functionality to:
    - Initialize and maintain persistent session-based counters
    - Increment and decrement cell counts via UI interactions
    - Compute total leukocyte counts
    - Merge and retrieve all counted values as a single dictionary
    - Reset individual or all categories

    The tool is designed for digital microscopic differential counting,
    typically used in hematology education or laboratory workflows.
    """

    def __init__(self,count_times):
    
        self.count_times = count_times
        self.leukocyte_count_dict = {'Basophil': 0, 'Monozyt':0, 'Blast':0,'A':0,'Eosinophil':0,
                                'Lymphozyt':0,'Promyelozyt':0,'B':0,'Segmentierte':0,'Myelozyt':0,
                                'Plasmazelle':0,'Stabkernige':0,'Metamyelozyt':0}
        self.diverse_count_dict = {'Normoblast':0, 'C':0, 'D':0}

    def initialize_session_state(self): 
        """Initialize streamlit.session_state to add 'leukocyte_count' and 'diverse_count' into the corresponding count"""

        if self.count_times not in st.session_state:
            st.session_state[self.count_times] = {'leukocyte_count':self.leukocyte_count_dict, 'diverse_count' : self.diverse_count_dict}

    def get_total_leukocytes(self): 
        """
        Calculate total leukocyte count stored in session state.

        Returns:
            int: Sum of all values in leukocyte_count.
        """
        return sum(st.session_state[self.count_times]["leukocyte_count"].values())
    
    def get_increment_value(self, add_or_sub_count):
        """
        Convert action string into numeric increment/decrement value.

        Args:
            add_or_sub_count (str): Either "addieren" or "subtrahieren".

        Returns:
            int: +1 if "addieren", -1 if "subtrahieren".

        Raises:
            ValueError: If input is not "addieren" or "subtrahieren".
        """
        if add_or_sub_count == "addieren":
            increment = +1
        elif add_or_sub_count == "subtrahieren":
            increment = -1
        else:
            raise ValueError("Input can either be 'addieren' or 'subtrahieren'") 
            
        return increment

    def render_cell_column_buttons(self, list_of_input, variable):
        """
        Create Streamlit buttons for a column of cell types and update counts.

        Args:
            list_of_input (list[str]): List of cell type names to display as buttons.
            variable (int): Value to add or subtract from counts (+1 or -1).
        """
        for key_name in list_of_input:
            if st.button(key_name, use_container_width = True):
                if key_name not in ["Normoblast","D","C"]:
                    st.session_state[self.count_times]['leukocyte_count'][key_name] += variable
                else:
                    st.session_state[self.count_times]["diverse_count"][key_name] += variable

    def render_differential_counter(self, add_or_sub_count):
        """
        Streamlit-based Hematology Differential counting tool.

        Displays interactive buttons for different leukocyte and diverse cell types.
        Allows incrementing or decrementing counts depending on user input.

        Args:
            add_or_sub_count (str): Either "addieren" or "subtrahieren".
        """
        count = self.get_total_leukocytes()

        variable = self.get_increment_value(add_or_sub_count)

        col1, col2, col3, col4 = st.columns(4, gap="small")

        if count <= 99:
            with col1:
                self.render_cell_column_buttons(['Basophil','Monozyt','Blast','A'], variable = variable)
            with col2: 
                self.render_cell_column_buttons(['Eosinophil','Lymphozyt','Promyelozyt','B'], variable = variable)
            with col3: 
                self.render_cell_column_buttons(['Normoblast','Segmentierte','Myelozyt','C'], variable = variable)
            with col4: 
                self.render_cell_column_buttons(['Plasmazelle','Stabkernige','Metamyelozyt','D'], variable = variable)
        
        st.write(self.get_total_leukocytes())


    def get_combined_counts(self):
        """
        Merge leukocyte_count and diverse_count from Streamlit session state.

        Returns:
            dict: Combined dictionary of all counted cell types.
        """
        combined_counts = copy.deepcopy(st.session_state[self.count_times]["leukocyte_count"])
        for cell in st.session_state[self.count_times]["diverse_count"]:
            combined_counts[cell] = st.session_state[self.count_times]["diverse_count"][cell]
        return combined_counts
    
    def reset_category(self, category):
        """
        Reset all values in a given category inside session state.

        Args:
            category (str): Either "leukocyte_count" or "diverse_count".
        """
        for session in st.session_state[self.count_times][category]:
            st.session_state[self.count_times][category][session] = 0

    def reset_all_counts(self):
        """
        Reset all leukocyte and diverse cell counts in session state.
        """
        self.reset_category("leukocyte_count")
        self.reset_category("diverse_count")

