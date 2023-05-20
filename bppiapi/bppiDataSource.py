__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

from bppiapi.bppiApiWrapper import bppiApiWrapper
from utils.log import log
import pandas as pd
import constants as C
import time
from bppiapi.repConfig import repConfig
from utils.iniConfig import iniConfig
import json

MANDATORY_PARAM_LIST = [C.PARAM_BPPITOKEN, 
                        C.PARAM_BPPIURL]

class bppiDataSource:
    def __init__(self, config):
        self.__config = config          # All the configuration parameters
        self.__trace = None             # Logger
        self.__repositoryInfos = None   # BPPI Repository infos (gathered from the bppi server)

    # Contains all the config parameters (from the INI file)
    @property
    def config(self) -> iniConfig:
        return self.__config
    @property
    def mandatoryParameters(self) -> str:
        return MANDATORY_PARAM_LIST
    @property
    def repositoryConfig(self) -> repConfig:
        return self.__repositoryInfos
    @property
    def log(self) -> log:
        return self.__trace
    @property
    def url(self) -> str:
        return self.__serverURL
    @property
    def token(self) -> str:
        return self.__token

    @property
    def bppiTable(self) -> str:
        # Priority on what in inside the config file
        ini = self.config.getParameter(C.PARAM_BPPITABLE, C.EMPTY)
        return ini if (ini != C.EMPTY) else self.repositoryConfig.repositoryTableName
    @property
    def bppiTodos(self) -> str:
        # Priority on what in inside the config file
        ini = self.config.getParameter(C.PARAM_BPPITODOS, C.EMPTY).split(',')
        return ini if (ini != C.EMPTY) else self.repositoryConfig.todoLists

    def checkParameters(self) -> bool:
        """Check the mandatory parameters
        Returns:
            bool: False si at least one mandatory param is missing
        """
        try:
            for param in self.mandatoryParameters:
                if (self.config.getParameter(param, "") == ""):
                    self.log.error("Parameter <{}> is missing".format(param))
                    return False 
            return True
        except:
            self.log.error("checkParameters() Error")
            return False
    
    def initialize(self) -> bool:
        """Initialize the Class instance by gathering the BPPI repository infos.
            * initialize the logger
            * check the mandatory parameters
            * init the API (get the BPPI Repository infos)
        Returns:
            bool: False if error
        """
        try:
            # Init logger
            logfilename = self.config.getParameter(C.PARAM_LOGFOLDER, "") + self.config.getParameter(C.PARAM_LOGFILENAME, C.TRACE_FILENAME)
            print("Log file: {}".format(logfilename))
            level = self.config.getParameter(C.PARAM_LOGLEVEL, C.TRACE_DEFAULT_LEVEL)
            format = self.config.getParameter(C.PARAM_LOGFORMAT, C.TRACE_DEFAULT_FORMAT)
            self.__trace = log(__name__, logfilename, level, format)
            
            self.__trace.info("*** Check Configuration from the server ***")
            if (not self.checkParameters()):
                raise Exception("Some mandatory parameters are missing")
            api = bppiApiWrapper(self.config.getParameter(C.PARAM_BPPITOKEN), 
                                 self.config.getParameter(C.PARAM_BPPIURL))
            api.log = self.__trace
            # 1 - Get the repository configuration infos
            self.__repositoryInfos = api.getRepositoryConfiguration()
            return True
        except Exception as e:
            self.log.error("initialize() Error -> " + str(e))
            return False

    def terminate(self) -> bool:
        # For surcharge
        return True

    def executeToDo(self) -> bool:
        """Execute a BPPI TO DO (be careful as this TO DO must exists)
        Returns:
            bool: False if error or the TO DO does not exists
        """
        try:
            api = bppiApiWrapper(self.config.getParameter(C.PARAM_BPPITOKEN), 
                                 self.config.getParameter(C.PARAM_BPPIURL))
            api.log = self.log
            self.log.info("Execute these TO DO: {}".format(",".join(self.bppiTodos)))
            if (self.repositoryConfig.loaded):
                if (len(self.bppiTodos) > 0):
                    processId = api.executeTODO(self.repositoryConfig.repositoryId, 
                                                self.bppiTodos, 
                                                self.bppiTable)
                    self.waitForEndOfProcessing(processId)
                    self.log.info("To Do executed successfully")
                    return True
                else:
                    self.log.info("No configured To Do to execute")
                    return False
        except Exception as e:
            self.log.error("executeToDo() Error -> " + str(e))
            return False

    def getStatus(self, processingId) -> str:
        """Return the status of a process launched on the BPPI server
        Args:
            processingId (_type_): ID of the BPPI Process
        Returns:
            str: Process status (from BPPI server)
        """
        api = bppiApiWrapper(self.config.getParameter(C.PARAM_BPPITOKEN), 
                             self.config.getParameter(C.PARAM_BPPIURL))
        api.log = self.log
        return api.getProcessingStatus(processingId)

    def waitForEndOfProcessing(self, processId) -> str:
        """Wait for the end of the BPPI process execution
        Args:
            processId (_type_): ID of the BPPI Process
        Returns:
            str: Final Status
        """
        try:
            self.log.info("Wait for the end of a process execution")
            EndOfWait = True
            nbIterations = 0
            api = bppiApiWrapper(self.config.getParameter(C.PARAM_BPPITOKEN), 
                                 self.config.getParameter(C.PARAM_BPPIURL))
            api.log = self.log
            while (EndOfWait):
                # 5 - Check the status to veriify if the task is finished
                status = self.getStatus(processId)
                if ((status != C.API_STATUS_IN_PROGRESS) or (nbIterations > C.API_NB_ITERATION_MAX)):
                    EndOfWait = False
                time.sleep(C.API_WAIT_DURATION_SEC)
                nbIterations += 1
            return status
        except Exception as e:
            self.log.error("waitForEndOfProcessing() Error -> " + str(e))
            return C.API_STATUS_ERROR
    
    def collectData(self) -> pd.DataFrame: 
        """This method must be surchaged and aims to collect the data from the datasource to provides the corresponding dataframe
        Returns:
            pd.DataFrame: Dataset in a pd.Dataframe object
        """
        return pd.DataFrame()

    def alterData(self, df) -> pd.DataFrame: 
        """ Surcharge this method to enable modification in the Dataset after gathering the data and before uploding them in BPPI
            By default just manage the event mapping.
        Args:
            df (pd.DataFrame): source dataset
        Returns:
            pd.DataFrame: altered dataset
        """
        return self.eventMap(df)

    def eventMap(self, df) -> pd.DataFrame:
        """ Map the events with the dataset (in parameter df). 
            Event Map file:
                * CSV format + Header
                * Name in the C.PARAM_EVENTMAPTABLE
                * Column to map with the event map file  in the C.PARAM_EVENTMAPNAME field (orginal dataset)
                * Only 2 columns in the event map file: 
                    - col 1: source event name (the one to map with the source dataset)
                    - col 2: new event name (the one to use for event replacement)
            Mapping Rules:
                * Replace the Col1 per col2 every time (event name replacement)
                * If Col2 empty -> remove the row (revome not necessary events)
        Args:
            df (pd.DataFrame): Data Source
        Returns:
            pd.DataFrame: Data altered with the new events & remove the unecesserary ones
        """
        try:
            dfAltered = df
            if (self.config.getParameter(C.PARAM_EVENTMAP, C.NO) == C.YES):
                # Get parameters
                self.log.info("Map the events with the original dataset and the event map table")
                evtMapFilename = self.config.getParameter(C.PARAM_EVENTMAPTABLE)
                if (evtMapFilename == ""):
                    raise Exception("No Event map filename (CSV) was specified")
                evtMapColumnname = self.config.getParameter(C.PARAM_EVENTMAPNAME)
                if (evtMapColumnname == ""):
                    raise Exception("No Event column name (in the data source) was specified")
                # Open the event map file (assuming 1st col -> Original Event, 2nd col -> event altered or if nothing to remove)
                dfevtMap = pd.read_csv(evtMapFilename, encoding=C.ENCODING)
                if (dfevtMap.shape[1] != 2):
                    raise Exception("There are more than 2 columns in the event map file.")
                dfevtMap.rename(columns={dfevtMap.columns[0]:evtMapColumnname}, inplace=True)
                originalRecCount = df.shape[0]
                self.log.debug("There are {} records in the original dataset".format(originalRecCount))
                dfAltered = pd.merge(df, dfevtMap, on=evtMapColumnname, how ="inner")
                # Reshape the dataset (columns changes)
                del dfAltered[evtMapColumnname]
                dfAltered.rename(columns={dfevtMap.columns[1]: evtMapColumnname}, inplace=True)
                iNbRemoved = originalRecCount - dfAltered.shape[0]
                if (iNbRemoved != 0):
                    self.log.warning("{} records have been removed ".format(iNbRemoved))
            return dfAltered
        
        except Exception as e:
            self.log.error("eventMap() Error -> " + str(e))
            return super().alterData(df)

    def upload(self, dfDataset) -> bool:
        """ Upload a dataset (Pandas DataFrame) in the BPPI repository (in one transaction)
        Args:
            dfDataset (pd.DataFrame): DataFrame with the Data to upload
        Returns:
            bool: False if error
        """
        try:
            self.log.info("Upload the data into the BPPI repository in one transaction")
            api = bppiApiWrapper(self.config.getParameter(C.PARAM_BPPITOKEN), 
                                 self.config.getParameter(C.PARAM_BPPIURL))
            api.log = self.log
            if (self.repositoryConfig.loaded):
                fileKeys = []
                blocIdx, blocIdxEnd = 0, 0
                datasize = dfDataset.shape[0]
                if (datasize > C.API_BLOC_SIZE_LIMIT):
                    self.log.info("Data (all) size (Nb Lines= {}) is larger than the upload limit {}, split the data in several data blocs".format(datasize , C.API_BLOC_SIZE_LIMIT))
                    blocNum = 1
                    while (blocIdxEnd < len(dfDataset)-1):
                        # Create the blocs (Nb of line to API_BLOC_SIZE_LIMIT)
                        blocIdxEnd = blocIdx + C.API_BLOC_SIZE_LIMIT - 1
                        if (blocIdxEnd >= len(dfDataset)-1):
                            blocIdxEnd = len(dfDataset)-1
                        self.log.debug("Data bloc N°{}, Index from {} -> {}".format(blocNum, blocIdx, blocIdxEnd))
                        blocData = dfDataset.iloc[blocIdx:blocIdxEnd:,:]
                        blocIdx += C.API_BLOC_SIZE_LIMIT 
                        # 2 - Prepare the upload
                        uploadCfg = api.prepareUpload(self.repositoryConfig.repositoryId)
                        # 3 - Upload the file to the server
                        blocData_toupload = blocData.to_csv(header=True, encoding=C.ENCODING, index=False)
                        uploadOK = api.uploadData(blocData_toupload, uploadCfg.url, uploadCfg.headers)
                        fileKeys.append(uploadCfg.key)
                        if (uploadOK):
                            self.log.info("Data bloc N°{} was uploaded successfully".format(blocNum))
                        else:
                            self.log.warning("Data bloc N°{} was NOT uploaded successfully".format(blocNum))
                            break
                else:
                    self.log.debug("The data can be uploaded in one unique bloc")
                    # 2 - Prepare the complete file upload
                    uploadCfg = api.prepareUpload(self.repositoryConfig.repositoryId)
                    fileKeys.append(uploadCfg.key)
                    blocData_toupload = dfDataset.to_csv(header=True, encoding=C.ENCODING, index=False)
                    uploadOK = api.uploadData(blocData_toupload, uploadCfg.url, uploadCfg.headers)
                    keys = uploadCfg.key
                    if (uploadOK):
                        self.log.info("Data was uploaded successfully")
                    else:
                        self.log.warning("Data was NOT uploaded successfully")
                keys = json.dumps(fileKeys)
                if (uploadOK):
                    self.log.info("Load the uploaded data/bloc(s) into the BPPI repository")
                    # 4 - Load the file into the BPPI repository
                    processId = api.loadFileToBPPIRepository(self.repositoryConfig.repositoryId, keys, self.bppiTable)
                    self.waitForEndOfProcessing(processId)
                else:
                    self.log.error("The data have not been loaded successfully")
            return True
        
        except Exception as e:
            self.log.error("upload() Error -> " + str(e))
            return False