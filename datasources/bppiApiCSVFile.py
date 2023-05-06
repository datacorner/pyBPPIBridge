__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import constants as C
from bppiapi.bppiApiParent import bppiApiParent
import pandas as pd

CSV_MANDATORY_PARAM_LIST = [C.PARAM_FILENAME, 
                            C.PARAM_BPPITOKEN, 
                            C.PARAM_BPPIURL]

class bppiApiCSVFile(bppiApiParent):

    def __init__(self, config):
        super().__init__(config)

    @property
    def mandatoryParameters(self) -> str:
        return CSV_MANDATORY_PARAM_LIST

    def initialize(self) -> bool:
        return super().initialize()

    def alterData(self, df) -> pd.DataFrame:
        return super().alterData(df)

    def collectData(self) -> pd.DataFrame: 
        """Read the CSV file and build the dataframe
        Returns:
            pd.DataFrame: Dataframe with the source data
        """
        try:
            filename = self.config.getParameter(C.PARAM_FILENAME)
            separator = self.config.getParameter(C.PARAM_CSV_SEPARATOR, ",")
            # Read the CSV file and provides a DataFrame
            df = pd.read_csv(filename, encoding=C.ENCODING, delimiter=separator)
            return df
        except Exception as e:
            self.log.error("collectData() Error" + str(e))
            return super().collectData()
        