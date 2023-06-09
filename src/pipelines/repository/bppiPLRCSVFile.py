__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import utils.constants as C
from bppiapi.repository.bppiRepository import bppiRepository
import pandas as pd

CSV_MANDATORY_PARAM_LIST = [C.PARAM_FILENAME]

""" Manages the CSV file extraction interface
    Class hierarchy:
    - bppiapi.bppiPipeline
        - bppiapi.repository.bppiRepository
            - pipelines.repository.bppiPLRCSVFile
"""
class bppiPLRCSVFile(bppiRepository):

    def __init__(self, config):
        super().__init__(config)

    @property
    def mandatoryParameters(self) -> str:
        return CSV_MANDATORY_PARAM_LIST

    def initialize(self) -> bool:
        return super().initialize()

    def transform(self, df) -> pd.DataFrame:
        return super().transform(df)

    def extract(self) -> pd.DataFrame: 
        """Read the CSV file and build the dataframe
        Returns:
            pd.DataFrame: Dataframe with the source data
        """
        try:
            filename = self.config.getParameter(C.PARAM_FILENAME)
            separator = self.config.getParameter(C.PARAM_CSV_SEPARATOR, C.DEFCSVSEP)
            # Read the CSV file and provides a DataFrame
            df = pd.read_csv(filename, encoding=C.ENCODING, delimiter=separator)
            return df
        except Exception as e:
            self.log.error("extract() Error" + str(e))
            return super().extract()
        