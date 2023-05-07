__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import constants as C
from datasources.bppiApiODBC import bppiApiODBC
import pandas as pd
import xml.etree.ElementTree as ET
import warnings
import numpy as np
from string import Template
import pathlib

warnings.filterwarnings('ignore')

BP_MANDATORY_PARAM_LIST = [C.PARAM_CONNECTIONSTRING, 
                           C.PARAM_BPPITOKEN, 
                           C.PARAM_BPPIURL, 
                           C.PARAM_BPPROCESSNAME]

class bppiApiBluePrism(bppiApiODBC):
    def __init__(self, config):
        super().__init__(config)

    @property
    def mandatoryParameters(self) -> str:
        return BP_MANDATORY_PARAM_LIST
    @property
    def query(self) -> str:
        return self.__buildQuery()
    
    def initialize(self) -> bool:
        return super().initialize()
    
    def __buildQuery(self) -> str:
        """Build the SQL Query to get the BP logs against the BP repository
            The BP Logs SQL qeury is stored in the bp.config file and can be customized with 3 args:
                * {attrxml}: Name of the INPUT/OUTPUT attributes columns (XML format)
                * {processname}: Process Name in Blue Prism
                * {stagetypefilter}: list of stage to filter out
                * {delta}: Delta loading condition on datetime (Between or < >)
                * {tablelog}: Name of the Log table (unicode or not unicode)
        Returns:
            str: built SQL Query
        """
        try: 
            processname = self.config.getParameter(C.PARAM_BPPROCESSNAME)
            stagetypes = self.config.getParameter(C.PARAM_BPSTAGETYPES)
            if (len(stagetypes) == 0):
                stagetypes = "0"
            # Get the query skeleton in the sql file
            sqlTemplate = Template(pathlib.Path(C.BPLOG_INI4SQL).read_text())
            # Build the filters on the VBO only
            novbo = "1=1"
            if (self.config.getParameter(C.PARAM_BPINCLUDEVBO, C.YES) != C.YES):
                novbo = "processname IS NULL"
            # Add the delta extraction filters if required (-fromdate and/or -todate filled)
            fromdate = self.config.getParameter(C.PARAM_FROMDATE)
            todate = self.config.getParameter(C.PARAM_TODATE)
            deltasql = "1=1"
            if ((fromdate != C.EMPTY) and (todate != C.EMPTY)):
                deltasql = "AND LOG.startdatetime BETWEEN '" + fromdate + "' AND '" + todate + "'"
            elif (fromdate != C.EMPTY):
                deltasql = "AND LOG.startdatetime > '" + fromdate + "'"
            elif (todate != C.EMPTY):
                deltasql = "AND LOG.startdatetime < '" + todate + "'"
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
            self.log.error("__buildQuery() -> Unable to build the Blue Prism Query " + str(e))
            return ""
        
    def __parseAttrs(self, logid, attribute, dfattributes) -> pd.DataFrame:
        """ Parse the attributexml field and extract (only) the text data (not the collection)
        Args:
            logid (str): ID of the log line (for later merge)
            attribute (str): attributexml value (XML format)
            dfattributes (DataFrame): Dataframe with tne incremental parameters added into

        Returns:
            pd.DataFrame: _description_
        """
        try:
            #    Blue Prism Log Format expected:
            #    <parameters>
            #        <inputs>
            #            <input name="Nom" type="text" value="Benoit Cayla" />
            #            ...
            #        </inputs>
            #        <outputs>
            #            <output name="Contact Form" type="flag" value="True" />
            #            ...
            #        </outputs>
            #    </parameters>
            root = ET.fromstring(attribute)
            if (root.tag == "parameters"):
                for input in root.findall("./inputs/input"):
                    if (input.attrib["type"] == "text"):    # only get the text input parameters
                        df_new_row = pd.DataFrame.from_records({'logid': logid, 'Name' : input.attrib["name"], 'value' :input.attrib["value"], 'in_out' : 'I'}, index=[0])
                        dfattributes = pd.concat([dfattributes, df_new_row])
                for output in root.findall("./outputs/output"):
                    if (output.attrib["type"] == "text"):    # only get the text output parameters
                        df_new_row = pd.DataFrame.from_records({'logid': logid, 'Name' : output.attrib["name"], 'value' :output.attrib["value"], 'in_out' : 'O'}, index=[0])
                        dfattributes = pd.concat([dfattributes, df_new_row]) 
            return dfattributes
        except Exception as e:
            self.log.error("__parseAttrs() -> Unable to parse the BP Attribute " + str(e))
            return dfattributes

    def __getAttributesFromLogs(self, df) -> pd.DataFrame:
        """Extract the logs (especially the parameters from the logs which are stored in XML format)
            Note: if no parameters in the list, no import
        Args:
            df (Dataframe): Dataframe with the logs
            config (bppiapi.iniConfig): list of parameters from the INI file
        Returns:
            DataFrame: logs altered with parameters
        """
        parameters = self.config.getParameter(C.PARAM_BPPARAMSATTR, C.EMPTY)
        # Manage the IN/OUT parameters from the logs
        if (len(parameters) > 0):
            # Extract the input and output parameters
            self.log.info("Extract the input and output parameters")
            dfattributes = pd.DataFrame(columns= ["logid", "Name", "value", "in_out"])
            for index, row in df.iterrows():
                if (row[C.BPLOG_ATTRIBUTE_COL] != None):
                    dfattributes = self.__parseAttrs(row["logid"], row[C.BPLOG_ATTRIBUTE_COL], dfattributes)
            self.log.debug("Attributes found: {}".format(str(dfattributes.shape[0])))
            # Only keep the desired parameters
            self.log.debug("Filter the desired parameters")
            # Build the filter with the parameters list
            params = [ "\"" + x + "\"" for x in parameters.split(",") ]
            paramQuery = "Name in (" + ",".join(params) + ")"
            dfattributes = dfattributes.query(paramQuery)
            self.log.debug("Attributes filtered: {}".format(str(dfattributes.shape[0])))
            # Pivot the parameter values to create one new column per parameter
            self.log.info("Build the final dataset with parameters")
            # add the IN or OUT parameter (the commented line below creates 2 differents parameters if the same param for IN and OUT)
            dfattributes['FullName'] = dfattributes['Name']
            dfattributesInCols = pd.pivot_table(dfattributes, values='value', index=['logid'], columns=['FullName'], aggfunc=np.sum, fill_value="")
            dfattributesInCols.reset_index()
            # Merge the Dataframes
            dffinal = df.merge(dfattributesInCols, on="logid", how='left')
            dffinal = dffinal.drop(C.BPLOG_ATTRIBUTE_COL, axis=1)
            return dffinal
        else:
            df

    def alterData(self, df) -> pd.DataFrame:
        """Alter the gathered data (from the BP Repository) by managing the attributes (stored in a XML format)
        Args:
            df (pd.DataFrame): Data source
        Returns:
            pd.DataFrame: Altered dataset with the selected parameters as new columns
        """
        # Filter out the df by selecting only the Start & End (main page / process) stages if requested
        if (self.config.getParameter(C.PARAM_BPFILTERSTEND) == C.YES):
            mainpage = self.config.getParameter(C.PARAM_BPMAINPROCESSPAGE, C.BP_MAINPAGE_DEFAULT) 
            # Remove the logs with stagename = "End" outside the "Main Page"
            oldCount = df.shape[0]
            df = df[~((df[C.BPLOG_STAGENAME_COL] == C.BP_STAGE_END) & (df[C.BPLOG_PAGENAME_COL] != mainpage))]
            self.log.info("{} records have been removed (No <End> stage outside the Main Process Page)".format(oldCount - df.shape[0]))
            # Remove the logs with stagename = "Start" outside the "Main Page"
            oldCount = df.shape[0] 
            df = df[~((df[C.BPLOG_STAGENAME_COL] == C.BP_STAGE_START) & (df[C.BPLOG_PAGENAME_COL] != mainpage))]
            self.log.info("{} records have been removed (No <Start> stage outside the Main Process Page)".format(oldCount - df.shape[0]))
        # Get the attributes from the BP logs
        df = self.__getAttributesFromLogs(df)
        return super().alterData(df)