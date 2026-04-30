import pandas as pd
from datetime import datetime, timezone

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
                - "Speicherzeit" (str): Current UTC timestamp in ISO format.
                - "Legend" (str): Description or legend associated with the dataset.
        """
        return {"Speicherzeit" : datetime.now(timezone.utc).isoformat(), "Legend": self.legend}
    
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
                        "data": {...},
                        "meta_info": {...}
                    }
                }
        """       
        return {self.id : {"data": self. _build_data(), "meta_info": self._build_meta_info()}}
    
class DisplayFormatter:
    pass