import pandas as pd
from datetime import datetime, timezone
import plotly.express as px

class StorageFormatter:
    """
    Format blood smear analysis data into a structured dictionary
    suitable for persistent storage (e.g., JSON files or databases).

    This class combines:
    - Quantitative count data from a pandas DataFrame
    - Morphological assessments of blood cells
    - Metadata such as timestamp and descriptive legend

    The output is a nested dictionary keyed by a unique identifier,
    ensuring consistent structure for downstream storage or processing.

    Attributes:
        id (int): Unique identifier for the dataset.
        df_count (pd.DataFrame): DataFrame containing count data of the blood smear.
        ec_morph (str): Morphological description of erythrocytes.
        lc_morph (str): Morphological description of leukocytes.
        tc_morph (str): Morphological description of thrombocytes.
        legend (str): Additional descriptive information or legend for the dataset.

    Typical usage:
        formatter = StorageFormatter(id, df, ec, lc, tc, legend)
        data_dict = formatter.to_dict()
    """
    
    def __init__(self, id: int, df_count: pd.DataFrame , ec_morph: str, lc_morph: str, tc_morph: str, legend: str):
        """
        Initialize the object.

        Args:
            id (int): Unique identifier for the instance.
            df_count (pd.DataFrame): DataFrame containing count data of a blood smear.
            ec_morph (str): EC morphology describtion.
            lc_morph (str): LC morphology describtion.
            tc_morph (str): TC morphology describtion.
        """
        
        self.id = id
        self.df_count = df_count
        self.ec_morph = ec_morph
        self.lc_morph = lc_morph
        self.tc_morph = tc_morph
        self.legend = legend
        
    def _build_meta_info(self):
        """
        Generate metadata information for the current dataset.

        Returns:
            dict: Metadata containing:
                - "save_time" (str): Current UTC timestamp in ISO format.
                - "Legend" (str): Description or legend associated with the dataset.
        """
        return {"save_time" : datetime.now(timezone.utc).isoformat(), "legend": self.legend}
    
    def  _build_data(self):
        """
        Prepare the core data for storage.

        This includes:
        - The counted values from the DataFrame.
        - Morphological descriptions for erythrocytes, leukocytes, and thrombocytes.

        Returns:
            dict: Structured data containing:
                - "count" (dict): Serialized DataFrame with count data.
                - "morph" (dict): Morphological assessments.
        """
        dict_morph = {"Erythrozyten Beurteilung": self.ec_morph, "Leukozyten Beurteilung": self.lc_morph, "Thrombozyten Beurteilung": self.tc_morph }
        return {"count": self.df_count.to_dict("split"), "morph": dict_morph}

    def to_dict(self): 
        """
        Combine data and metadata into a single dictionary structure
        ready for storage (e.g., JSON or database).

        The output is keyed by the instance ID.

        Returns:
            dict: Final structured dictionary in the format:
                {
                    <id>: {
                        "raw_data": {...},
                        "meta_info": {...}
                    }
                }
        """       
        return {self.id : {"raw_data": self. _build_data(), "meta_info": self._build_meta_info()}}

class DisplayFormatter:
    """Organizes stored data and presents it in various formats."""
    
    def __init__(self, user_data):
        """
        Initialize the DisplayFormatter.

        Args:
            user_data (dict): A dictionary containing:
                
                - "raw_data" (dict): Processed data, expected to include a
                  "count" key with table-like structure:
                      * "index" (list): Row labels
                      * "columns" (list): Column names
                      * "data" (list of lists): Row-wise data
                
                - "meta_info" (dict): Additional metadata related to the data.

        Example:
            {
                "raw_data": {
                    "count": {
                        "index": [0, 1],
                        "columns": ["A", "B"],
                        "data": [
                            [1, 2],
                            [3, 4]
                        ]
                    }
                },
                "meta_info": {
                    "source": "generated"
                }
            }
        """
        self.raw_data = user_data["raw_data"]
        self.meta_info = user_data["meta_info"]
    
    def get_count_data(self):
        """
        Retrieve count data components from raw_data.

        Returns:
            tuple: (index, columns, data)
        """
        count_data = self.raw_data["count"]
        
        return (count_data["index"], count_data["columns"], count_data["data"])
    
    def get_morph_data(self):
        """
        Retrieve morphological data components from raw_data.

        Returns:
            dict: ("Erythrozyten Beurteilung, "Leukozyten Beurteilung", "Thrombozyten Beurteilung")
        """
        
        return self.raw_data["morph"]
    
    def get_meta_info(self):
        """
        Retrieve morphological data components from raw_data.

        Returns:
            tuple: (legend, save_time)
        """ 
        legend = self.meta_info["legend"]
        save_time = self.meta_info["save_time"]
        
        if legend == "":
            legend = "Keine Angaben"
        
        return (legend, save_time)
        
    def to_dataframe(self):
        """
        Convert the stored count data into a pandas DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame constructed from the "count"
            data inside `raw_data`, using its index, columns, and values.
        """
        index, columns, data = self.get_count_data()
        return pd.DataFrame(data = data, columns = columns, index = index)
    
    def to_pie_plot(self, values_col="Mittelwert", title="Mittelwert der Leukozytenverteilung"):
        """
        Create a pie chart from the stored data.

        Args:
            values_col (str): Column to use for slice sizes.
            title (str): Title of the chart.

        Returns:
            plotly.graph_objects.Figure: A Plotly pie chart.
        """
        df = self.to_dataframe()
        return px.pie(df, values = values_col, names = df.index.tolist(), title = title)
    
        