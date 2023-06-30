__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import configparser
import utils.constants as C

SECTION_PARAM_SEP = "."

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
            self.__config = configparser.ConfigParser()
            self.__config.read(filename)
            for section in self.__config:
                for param in self.__config[section]:
                    try :
                        self.__parameters[section + SECTION_PARAM_SEP + param] = self.__config[section][param]
                    except:
                        self.__parameters[section + SECTION_PARAM_SEP + param] = C.EMPTY
            return True
        except Exception as e:
            print("loadini() -> " + str(e))
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