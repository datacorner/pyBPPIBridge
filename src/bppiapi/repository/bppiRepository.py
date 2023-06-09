__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

from bppiapi.repository.bppiApiRepositoryWrapper import bppiApiRepositoryWrapper
from bppiapi.bppiPipeline import bppiPipeline
import utils.constants as C
from bppiapi.repository.repConfig import repConfig
import json

MANDATORY_PARAM_LIST = [C.PARAM_BPPITOKEN, 
                        C.PARAM_BPPIURL]

class bppiRepository(bppiPipeline):
    def __init__(self, config):
        super().__init__(config)
        self.__repositoryInfos = None   # BPPI Repository infos (gathered from the bppi server)

    @property
    def repositoryConfig(self) -> repConfig:
        return self.__repositoryInfos

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
    
    def initialize(self) -> bool:
        """Initialize the Class instance by gathering the BPPI repository infos.
            * initialize the logger
            * check the mandatory parameters
            * init the API (get the BPPI Repository infos)
        Returns:
            bool: False if error
        """
        try:
            super().initialize()
            # Get the repository configuration infos
            api = bppiApiRepositoryWrapper(self.config.getParameter(C.PARAM_BPPITOKEN), 
                                           self.config.getParameter(C.PARAM_BPPIURL))
            api.log = super().log
            self.__repositoryInfos = api.getRepositoryConfiguration()
            return True
        except Exception as e:
            self.log.error("initialize() Error -> " + str(e))
            return False

    def executeToDo(self) -> bool:
        """Execute a BPPI TO DO (be careful as this TO DO must exists)
        Returns:
            bool: False if error or the TO DO does not exists
        """
        try:
            api = bppiApiRepositoryWrapper(self.config.getParameter(C.PARAM_BPPITOKEN), 
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

    def load(self, dfDataset) -> bool:
        """ Upload a dataset (Pandas DataFrame) in the BPPI repository (in one transaction)
        Args:
            dfDataset (pd.DataFrame): DataFrame with the Data to upload
        Returns:
            bool: False if error
        """
        try:
            self.log.info("Upload the data into the BPPI repository in one transaction")
            api = bppiApiRepositoryWrapper(self.config.getParameter(C.PARAM_BPPITOKEN), 
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