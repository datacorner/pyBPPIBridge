import constants as C
from bppiapi.bppiApiParent import bppiApiParent
import pandas as pd

EXCEL_MANDATORY_PARAM_LIST = [C.PARAM_FILENAME, 
                              C.PARAM_EXCELSHEETNAME, 
                              C.PARAM_BPPITOKEN, 
                              C.PARAM_BPPIURL]

class bppiApiExcelFile(bppiApiParent):

    def __init__(self, config):
        super().__init__(config)

    @property
    def mandatoryParameters(self) -> str:
        return EXCEL_MANDATORY_PARAM_LIST

    def initialize(self) -> bool:
        return super().initialize()

    def alterData(self, df) -> pd.DataFrame:
        return super().alterData(df)

    def collectData(self) -> pd.DataFrame: 
        """Read the Excel file and build the dataframe
        Returns:
            pd.DataFrame: Dataframe with the source data
        """
        try:
            filename = self.config.getParameter(C.PARAM_FILENAME)
            sheet = self.config.getParameter(C.PARAM_EXCELSHEETNAME)
            if (sheet == "0" or sheet == ""):
                sheet = 0
            # Read the Excel file and provides a DataFrame
            df = pd.read_excel(filename, sheet_name=sheet)
            return df
        except Exception as e:
            self.log.error("collectData() Error" + str(e))
            return super().collectData()
        