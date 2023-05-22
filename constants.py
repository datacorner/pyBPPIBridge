__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import logging

ENCODING = "utf-8"
YES = "yes"
NO = "no"
EMPTY = ""
DEFCSVSEP = ","

# Parameter Names
PARAM_SRCTYPE = "sourcetype"                            # Data source type {csv|excel|odbc|blueprism}
PARAM_SRCTYPE_VALCSV = "csv"                            # sourcetype = csv
PARAM_SRCTYPE_VALXES = "xes"                            # sourcetype = xes
PARAM_SRCTYPE_VALODBC = "odbc"                          # sourcetype = odbc
PARAM_SRCTYPE_VALBP = "blueprism"                       # sourcetype = blueprism
PARAM_SRCTYPE_VALXLS = "excel"                          # sourcetype = excel
PARAM_SRCTYPE_VALSAPTABLE = "saptable"                  # sourcetype = SAP RFC Table
PARAM_SRCTYPE_SUPPORTED = [PARAM_SRCTYPE_VALCSV,
                           PARAM_SRCTYPE_VALODBC,
                           PARAM_SRCTYPE_VALXES,
                           PARAM_SRCTYPE_VALXLS,
                           PARAM_SRCTYPE_VALBP,
                           PARAM_SRCTYPE_VALSAPTABLE]
PARAM_FILENAME = "filename"                             # {csv|xes} Source file dataset
PARAM_CSV_SEPARATOR ="sep"                              # {csv} CSV fields separator (by default comma)
PARAM_CONFIGFILE = "configfile"                         # {odbc|blueprism} Config / INI file
PARAM_EXCELSHEETNAME = "sheet"                          # {excel} Excel spreadsheet name
# Parameters which can be in the INI file
PARAM_BPPITOKEN = "bppi.token"                          # {csv|xes|excel|odbc|blueprism} BPPI Token
PARAM_BPPIURL = "bppi.url"                              # {csv|xes|excel|odbc|blueprism} BPPI URL
PARAM_CONNECTIONSTRING = "database.connectionstring"    # {ODBC/Blue Prism} ODBC Connection String
PARAM_QUERY = "database.query"                          # {ODBC} Query to gather data
PARAM_FROMDATE = "fromdate"                             # {blueprism}From Date (delta extraction)
PARAM_TODATE = "todate"                                 # {blueprism}To Date (delta extraction)
PARAM_BPPROCESSNAME = "blueprism.processname"           # {blueprism} Process Name  (to gather the logs from)
PARAM_BPSTAGETYPES = "blueprism.stagetypefilters"       # {blueprism} filter out these stages (list of stages type separated by comma)
PARAM_BPINCLUDEVBO = "blueprism.includevbo"             # {blueprism} yes/no : Extract the VBO logs
PARAM_BPUNICODE = "blueprism.unicode"                   # {blueprism} yes/no : Blue Prism logs in unicode or not
PARAM_BPPITABLE = "bppi.table"                          # {odbc|blueprism} Name of the table in the BPPI repository
PARAM_BPPITODOACTIVED = "bppi.todos"                    # {csv|xes|excel|odbc|blueprism} Execute the to do (yes/no)
PARAM_BPPITODOS = "bppi.todolist"                       # {odbc|blueprism} List of BPPI TO DOs to execute after loading
PARAM_LOGFILENAME = "other.logfilename"                 # {csv|xes|excel|odbc|blueprism} Filename of the Log file
PARAM_LOGFOLDER = "other.logfolder"                     # {csv|xes|excel|odbc|blueprism} Folder to store the Logs
PARAM_LOGLEVEL = "other.loglevel"                       # {csv|xes|excel|odbc|blueprism} Log level (DEBUG|INFO|WARNING|ERROR)
PARAM_LOGFORMAT = "other.logformat"                     # {csv|xes|excel|odbc|blueprism} Log format (Cf. Python logger doc)
PARAM_BPPARAMSATTR = "blueprism.parameters"             # {blueprism} List (separated by a comma) of the BP parameters/attributes to gather (will be added in new columns)
PARAM_EVENTMAP = "events.map"                           # {odbc|blueprism} yes/no : manage event mapping
PARAM_EVENTMAPTABLE = "events.maptable"                 # {odbc|blueprism} Map the events with the dataset. This param contains the name of the csv file which stores the event map (col 1: source event name, col 2: new event name)
PARAM_EVENTMAPNAME = "events.column"                    # {odbc|blueprism} Name of the event column name in the original source
PARAM_BPFILTERSTEND = "blueprism.startendfilter"        # {blueprism} yes/no: filtr out all Start & End stages except the Main Page ones
PARAM_BPMAINPROCESSPAGE = "blueprism.mainprocesspage"   # {blueprism} BP Process Main Page name
PARAM_BPDELTA = "blueprism.delta"                       # {blueprism} delta load activated (yes/no), if no full load
PARAM_BPDELTA_FILE = "blueprism.deltafile"              # {blueprism} file where the latest date load is saved (for delta load only)
PARAM_SAP_ASHOST = "sap.ashost"                         # {saptable} AP Host name or IP
PARAM_SAP_CLIENT = "sap.client"                         # {saptable} SAP Client
PARAM_SAP_SYSNR = "sap.sysnr"                           # {saptable} SAP System Number
PARAM_SAP_USER = "sap.user"                             # {saptable} SAP User
PARAM_SAP_PASSWD = "sap.passwd"                         # {saptable} SAP Password
PARAM_SAP_ROUTER = "sap.saprouter"                      # {saptable} SAP Router (if any)
PARAM_SAP_RFC_TABLE = "sap.rfctable"                    # {saptable} RFC Table to request
PARAM_SAP_RFC_FIELDS = "sap.rfcfields"                  # {saptable} List of fields to gather (separated by a comma)
PARAM_SAP_RFC_ROWCOUNT = "sap.rowlimit"                 # {saptable} Row Count limit (Nb Max of rows retreived from SAP)

# BPPI API
API_1_0 = "/api/ext/1.0/"
API_REPOSITORY_CONFIG = "repository/repository-import-configuration"
API_SERVER_UPLOAD_INFOS = "repository/{}/file/upload-url"
API_SERVER_LOAD_2_REPO = "repository/{}/load"
API_PROCESSING_STATUS = "processing"
API_EXECUTE_TODO = "repository/{}/execute-todo-list"
API_WAIT_DURATION_SEC = 2
API_NB_ITERATION_MAX = API_WAIT_DURATION_SEC * 30
API_STATUS_IN_PROGRESS = "IN_PROGRESS"
API_STATUS_ERROR = "ERROR"
API_BLOC_SIZE_LIMIT = 10000 # Same limitation as the current API call via java

# Logger configuration
TRACE_DEFAULT_LEVEL = logging.DEBUG
TRACE_DEFAULT_FORMAT = "%(asctime)s|%(name)s|%(levelname)s|%(message)s"
TRACE_FILENAME = "bppiapiwrapper.log"
TRACE_MAXBYTES = 1000000

# Dump file suffix
TEMP_SQLDUMP = "-temp-sqlserver-dump.csv"

# Blue Prism stuff
BPLOG_STAGETYPE_COL = "stagetype"                   # Name of the stagetype column in the BP Repo
BPLOG_STAGENAME_COL = "stagename"                   # Name of the stagename column in the BP Repo
BPLOG_PAGENAME_COL = "pagename"                     # Name of the pagename column in the BP Repo
BPLOG_PROCESSNAME_COL = "processname"               # Name of the process name column in the BP Repo
BPLOG_STARTDATETIME_COL = "startdatetime"           # Name of the Start Date & time column in the BP Repo
BPLOG_ATTRIBUTE_COL = "attributexml"                # Name of the attributexml column in the BP Repo
BPLOG_LOG_UNICODE = "BPASessionLog_Unicode"         # BP Log table name for unicode
BPLOG_LOG_NONUNICODE = "BPASessionLog_NonUnicode"   # BP Log table name for non unicode
BPLOG_INI4SQL = "bplogs.sql"                        # File which contains the BP SQL Query
BP_STAGE_START = "Start"                            # Name of the BP Start stage
BP_STAGE_END = "End"                                # Name of the BP End stage
BP_MAINPAGE_DEFAULT = "Main Page"                   # Name of the BP Main Page (process)
BP_DEFAULT_DELTAFILE = "bpdelta.tag"                # Default filename for the delta tag
BP_DELTADATE_FMT = "%Y-%m-%d %H:%M:%S"              # Delta date format %Y-%m-%d %H:%M:%S