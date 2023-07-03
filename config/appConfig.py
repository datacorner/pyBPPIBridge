__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import configparser
import utils.constants as C
import sqlite3

SECTION_PARAM_SEP = "."

class cursorbyField(object):
    def __init__(self, cursor, row):
        for (attr, val) in zip((d[0] for d in cursor.description), row) :
            setattr(self, attr, val)

class appConfig():
    """This class contains all the configuration needed and loaded mainly from the INI file
    """


    def __init__(self):
        self.__parameters = {}
        return

    def addParameter(self, name, value):
        """Add a new parameter in the list
        Args:
            name (str): paramter name
            value (str): parameter value
        """
        try:
            self.__parameters[name] = value
        except Exception as e:
            print("addParameter() -> " + str(e))

    def loadFromINIFile(self, filename) -> bool:
        """ Load the configuration from the INI file in parameter
        Args:
            filename (str): INI file name
        Returns:
            bool: False if error
        """
        try:
            myConfig = configparser.ConfigParser()
            myConfig.read(filename)
            for section in myConfig:
                for param in myConfig[section]:
                    try :
                        self.__parameters[section + SECTION_PARAM_SEP + param] = myConfig[section][param]
                    except:
                        self.__parameters[section + SECTION_PARAM_SEP + param] = C.EMPTY
            return True
        except Exception as e:
            print("loadFromINIFile() -> " + str(e))
            return False

    def loadFromSQLite(self, db_file, id) -> bool:
        """ Load the configuration from the sqlite file in parameter
        Args:
            filename (str): sqlite3 file name
            id (str): id of the configuration
        Returns:
            bool: False if error
        """
        try:
            conn = sqlite3.connect(db_file)
            cur = conn.cursor()
            sql = "SELECT ID, PIPELINENAME, SERVERNAME, SERVERTOKEN, BPPITABLE, LOGFOLDER, LOGFILENAME, "
            sql += "LOGLEVEL, LOGFORMAT, BPPITODO, SRC, PROCESSNAME, INCVBO, UNICODE, STARTENDFILTER, "
            sql += "DELTA, DELTATAG, ODBCONN, QUERY, STAGEFILTERLIST, PARAMLIST"
            sql += " FROM VIEW_GET_FULLCONFIG_BLUEPRISM_REPO"
            sql += " WHERE ID={}".format(id)
            cur.execute(sql)
            rows = cur.fetchall()
            if (len(rows) == 1):
                r = cursorbyField(cur, rows[0])
                self.__parameters[C.PARAM_BPPIURL] = r.SERVERNAME
                self.__parameters[C.PARAM_BPPITOKEN] = r.SERVERTOKEN
            else:
                raise Exception ("There are more than one configuration (ore none) available.")

            return True
        except Exception as e:
            print("loadFromSQLite() -> " + str(e))
            return False

    def getParameter(self, parameter, default="") -> str:
        """ Returns the Parameter value based on the INI Section & parameter name.
            If the parameter comes from the INI file we use the SECTION_PARAM_SEP to separate the section with the parameter
        Args:
            parameter (str): INI parameter name (section.parameter)
            default (str): default value if not found (by default empty string)
        Returns:
            str: parameter value, empty if not found
        """
        try:
            splitParams = parameter.split(SECTION_PARAM_SEP)
            if (len(splitParams) == 2): # with section
                param = self.__parameters[splitParams[0] + SECTION_PARAM_SEP + splitParams[1]]
            else:
                param =  self.__parameters[parameter]
            return default if (param == None or param == "") else param
        except Exception as e:
            return default

    def setParameter(self, parameter, value):
        """ Surcharge the existing paramter with a new (but not persistent) value
        Args:
            parameter (str): parameter name
            value (str): new value
        """
        try:
            self.__parameters[parameter] = str(value)
        except Exception as e:
            pass