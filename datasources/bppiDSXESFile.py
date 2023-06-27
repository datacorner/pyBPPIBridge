__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import constants as C
from bppiapi.bppiRepository import bppiRepository
import pandas as pd
import pm4py

XES_MANDATORY_PARAM_LIST = [C.PARAM_FILENAME]

class bppiDSXESFile(bppiRepository):

    def __init__(self, config):
        super().__init__(config)

    @property
    def mandatoryParameters(self) -> str:
        return XES_MANDATORY_PARAM_LIST

    def initialize(self) -> bool:
        return super().initialize()

    def alterData(self, df) -> pd.DataFrame:
        return super().alterData(df)

    def collectData(self) -> pd.DataFrame: 
        """Read the XES file and build the dataframe
        Returns:
            pd.DataFrame: Dataframe with the source data
        """
        try:
            filename = self.config.getParameter(C.PARAM_FILENAME)
            log = pm4py.read_xes(filename, index=False)
            df = pm4py.convert_to_dataframe(log)
            return df
        except Exception as e:
            self.log.error("collectData() Error" + str(e))
            return super().collectData()
        