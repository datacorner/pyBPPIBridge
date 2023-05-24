__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import constants as C
import pathlib
from string import Template
import datetime

NO_FILTER = "1=1"

class blueprismSQLBuilder():
    def __init__(self, log, config):
        self.__log = log
        self.__config = config
        pass

    @property
    def log(self):
        return self.__log
    @property
    def config(self):
        return self.__config
    
    def getTemplate(self, filename):
        try:
            return Template(pathlib.Path(C.BPLOG_INI4SQL).read_text())
        except Exception as e:
            self.log.error("getTemplate() -> Error when reading the SQL template " + str(e))
            return ""
        
    def build(self, lastDeltaDate) -> str:
        """Build the SQL Query to get the BP logs against the BP repository
            The BP Logs SQL qeury is stored in the bp.config file and can be customized with 3 args:
                * {attrxml}: Name of the INPUT/OUTPUT attributes columns (XML format)
                * {processname}: Process Name in Blue Prism
                * {stagetypefilter}: list of stage to filter out
                * {delta}: Delta loading condition on datetime (Between or < >)
                * {tablelog}: Name of the Log table (unicode or not unicode)
        Args:
            lastDeltaDate (str): Date of the Last load (if delta requested / nothing if full load)
        Returns:
            str: built SQL Query
        """
        try: 
            processname = self.config.getParameter(C.PARAM_BPPROCESSNAME)
            stagetypes = self.config.getParameter(C.PARAM_BPSTAGETYPES, "0")

            # Get the query skeleton in the sql file
            sqlTemplate = self.getTemplate(C.BPLOG_INI4SQL)

            # Build the filters on the VBO only
            novbo = NO_FILTER
            if (self.config.getParameter(C.PARAM_BPINCLUDEVBO, C.YES) != C.YES):
                novbo = C.BPLOG_PROCESSNAME_COL + " IS NULL"

            # Date Filtering and/or DELTA vs FULL
            if (lastDeltaDate != ""):
                self.log.info("DELTA Load requested - from <" + str(lastDeltaDate) + ">")
                # DELTA LOAD (get date from file first)
                deltasql = " FORMAT(LOG." + C.BPLOG_STARTDATETIME_COL + ",'yyyy-MM-dd HH:mm:ss') >= '" + lastDeltaDate + "'"
            else:
                self.log.info("FULL Load requested")
                # FULL LOAD / Add the delta extraction filters if required (-fromdate and/or -todate filled)
                fromdate = self.config.getParameter(C.PARAM_FROMDATE)
                todate = self.config.getParameter(C.PARAM_TODATE)
                if ((fromdate != C.EMPTY) and (todate != C.EMPTY)):
                    deltasql = " FORMAT(LOG." + C.BPLOG_STARTDATETIME_COL + ",'yyyy-MM-dd HH:mm:ss') BETWEEN '" + fromdate + "' AND '" + todate + "'"
                elif (fromdate != C.EMPTY):
                    deltasql = " FORMAT(LOG." + C.BPLOG_STARTDATETIME_COL + ",'yyyy-MM-dd HH:mm:ss') >= '" + fromdate + "'"
                elif (todate != C.EMPTY):
                    deltasql = " FORMAT(LOG." + C.BPLOG_STARTDATETIME_COL + ",'yyyy-MM-dd HH:mm:ss') <= '" + todate + "'"

            # BP Logs in unicode ? (default no)
            if (self.config.getParameter(C.PARAM_BPUNICODE) == C.YES):
                tablelog = C.BPLOG_LOG_UNICODE
            else:
                tablelog = C.BPLOG_LOG_NONUNICODE
                
            # Finalize the SQL Query by replacing the parameters
            valuesToReplace = { 
                                "processname" : processname, 
                                "stagetypefilters" : stagetypes, 
                                "onlybpprocess" : novbo, 
                                "delta" : deltasql, 
                                "tablelog" : tablelog
                                }
            sqlUpdated = sqlTemplate.substitute(valuesToReplace)
            return sqlUpdated
        
        except Exception as e:
            self.log.error("build() -> Unable to build the Blue Prism Query " + str(e))
            return ""