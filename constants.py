import logging

ENCODING = "utf-8"
YES = "yes"
NO = "no"

# Parameter Names
PARAM_FILENAME = "filename"                             # Source file dataset
PARAM_CONFIGFILE = "configfile"                         # Config / INI file
PARAM_SRCTYPE = "sourcetype"                            # Data source type {csv|odbc|blueprism}
PARAM_SRCTYPE_VALCSV = "csv"
PARAM_SRCTYPE_VALODBC = "odbc"
PARAM_SRCTYPE_VALBP = "blueprism"
# Parameters which can be in the INI file
PARAM_LOGFILENAME = "other.logfilename"                 # Filename of the Log file
PARAM_BPPITOKEN = "bppi.token"                          # BPPI Token
PARAM_BPPIURL = "bppi.url"                              # BPPI URL
PARAM_CONNECTIONSTRING = "database.connectionstring"    # {ODBC/Blue Prism} ODBC Connection String
PARAM_QUERY = "database.query"                          # {ODBC} Query to gather data
PARAM_FROMDATE = "fromdate"                             # {Blue Prism}From Date (delta extraction)
PARAM_TODATE = "todate"                                 # {Blue Prism}To Date (delta extraction)
PARAM_BPPROCESSNAME = "blueprism.processname"           # {Blue Prism} Process Name  (to gather the logs from)
PARAM_BPSTAGETYPES = "blueprism.stagetypefilters"       # {Blue Prism} filter out these stages (list of stages type separated by comma)
PARAM_BPINCLUDEVBO = "blueprism.includevbo"             # {Blue Prism} yes/no : Extract the VBO logs
PARAM_BPUNICODE = "blueprism.unicode"                   # {Blue Prism}yes/no : Blue Prism logs in unicode or not
PARAM_BPPITABLE = "bppi.table"                          # Name of the table in the BPPI repository
PARAM_BPPITODOS = "bppi.todos"                          # List of BPPI TO DOs to execute after loading
PARAM_LOGFOLDER = "other.logfolder"                     # Folder to store the Logs
PARAM_BPPARAMSATTR = "blueprism.parameters"             # {Blue Prism} List (separated by a comma) of the BP parameters/attributes to gather (will be added in new columns)
PARAM_EVENTMAP = "events.map"                           # yes/no : manage event mapping
PARAM_EVENTMAPTABLE = "events.maptable"                 # Map the events with the dataset. This param contains the name of the csv file which stores the event map (col 1: source event name, col 2: new event name)
PARAM_EVENTMAPNAME = "events.column"                    # Name of the event column name in the original source
PARAM_BPFILTERSTEND = "blueprism.startendfilter"        #
PARAM_BPMAINPROCESSPAGE = "blueprism.mainprocesspage"

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
TRACE_LEVEL = logging.DEBUG
TRACE_FORMAT = "%(asctime)s|%(name)s|%(levelname)s|%(message)s"
TRACE_FILENAME = "bppiapiwrapper.log"
TRACE_MAXBYTES = 1000000

# Dump file suffix
TEMP_SQLDUMP = "-temp-sqlserver-dump.csv"

# Blue Prism stuff
BPLOG_STAGETYPE_COL = "stagetype"                   # Name of the stagetype column in the BP Repo
BPLOG_STAGENAME_COL = "stagename"                   # Name of the stagename column in the BP Repo
BPLOG_PAGENAME_COL = "pagename"                     # Name of the pagename column in the BP Repo
BPLOG_ATTRIBUTE_COL = "attributexml"                # Name of the attributexml column in the BP Repo
BPLOG_LOG_UNICODE = "BPASessionLog_Unicode"         # BP Log table name for unicode
BPLOG_LOG_NONUNICODE = "BPASessionLog_NonUnicode"   # BP Log table name for non unicode
BPLOG_INI4SQL = "bplogs.sql"                         # File which contains the BP SQL Query
BP_STAGE_START = "Start"
BP_STAGE_END = "End"
BP_MAINPAGE_DEFAULT = "Main Page"