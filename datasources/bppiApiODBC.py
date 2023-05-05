__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import constants as C
from datasources.bppiApiCSVFile import bppiApiCSVFile
import pyodbc
import pandas as pd

# Mandatory params to check
ODBC_MANDATORY_PARAM_LIST = [C.PARAM_CONNECTIONSTRING, 
                             C.PARAM_BPPITOKEN, 
                             C.PARAM_BPPIURL, 
                             C.PARAM_QUERY]

class bppiApiODBC(bppiApiCSVFile):
    def __init__(self, config):
        super().__init__(config)

    @property
    def mandatoryParameters(self) -> str:
        return ODBC_MANDATORY_PARAM_LIST

    @property
    def query(self) -> str:
        return self.config.getParameter(C.PARAM_QUERY).replace("\n", " ")
    
    def initialize(self) -> bool:
        return super().initialize()
    
    def alterData(self, df) -> pd.DataFrame:
        return super().alterData(df)
    
    def collectData(self) -> pd.DataFrame: 
        """Read the DB by executing the query and build the dataframe
        Returns:
            pd.DataFrame: Dataframe with the source data
        """
        tableResult = pd.DataFrame()
        try:
            self.log.info("Execute the ODBC Query and load the result into the BPPI repository")
            if (self.repositoryConfig.loaded):
                odbc = self.config.getParameter(C.PARAM_CONNECTIONSTRING)
                query = self.query
                sqlserverConnection = pyodbc.connect(odbc)
                self.log.debug("Connected to ODBC Data source")
                if (not sqlserverConnection.closed):
                    self.log.debug("Execute the query: {}".format(query))
                    tableResult = pd.read_sql(query, sqlserverConnection)
                    sqlserverConnection.close()
                    self.log.debug("Data read, close ODBC Data source connection")
            return tableResult
        except Exception as e:
            self.log.error("collectData() Error -> " + str(e))
            try:
                sqlserverConnection.close()
            except:
                return super().collectData()
            return super().collectData()