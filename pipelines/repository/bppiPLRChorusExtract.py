__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import constants as C
from pipelines.repository.bppiPLRCSVFile import bppiPLRCSVFile
import pandas as pd

CHORUSFILE_MANDATORY_PARAM_LIST = [C.PARAM_FILENAME, 
                                    C.PARAM_BPPITOKEN, 
                                    C.PARAM_BPPIURL]

class bppiPLRChorusExtract(bppiPLRCSVFile):

    def __init__(self, config):
        super().__init__(config)

    @property
    def mandatoryParameters(self) -> str:
        return CHORUSFILE_MANDATORY_PARAM_LIST

    def initialize(self) -> bool:
        return super().initialize()

    def alterData(self, df) -> pd.DataFrame:
        return super().alterData(df)

    def collectData(self) -> pd.DataFrame: 
        return super().collectData()
        