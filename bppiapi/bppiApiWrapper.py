__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import requests
import json
from bppiapi.repConfig import repConfig
from bppiapi.uploadConfig import uploadConfig
from utils.log import log
from urllib import request
import constants as C

class bppiApiWrapper:
    """This class acts as a gateway for the BPPI API calls
    """
    def __init__(self, token, serverURL):
        self.__token = token
        self.__serverURL = serverURL
        self.__log = None

    @property
    def log(self):
        return self.__log
    @log.setter   
    def log(self, value):
        self.__log = value

    @property
    def apiRootPath(self):
        return self.__serverURL + C.API_1_0
    @property
    def URL(self):
        return self.__serverURL
    @property
    def Token(self):
        return self.__token

    def getRepositoryConfiguration(self) -> repConfig:
        """ HTTP GET / Gather the repository details & config from the server
        Returns:
            repConfig: BPPI repository config
        """
        try: 
            # Get Api call for getting Repository informations
            self.log.info("Get Api call for getting Repository informations")
            url = self.apiRootPath + C.API_REPOSITORY_CONFIG
            self.log.debug("HTTP GET Request " + url)
            headers = {}
            headers["Authorization"] = "Bearer " + self.Token
            headers["content-type"] = "application/json"
            httpResponse = requests.get(url , headers=headers) 
            repositoryCfg = repConfig(httpResponse)
            self.log.debug("HTTP Response: {}".format(repositoryCfg.jsonContent))
            if (repositoryCfg.loaded):
                self.log.info("Information from BPPI Repository collected successfully")
            return repositoryCfg
        except Exception as e:
            self.log.error("getRepositoryConfiguration Error | " + str(e))
            return repConfig()

    def prepareUpload(self, repositoryId) -> uploadConfig:
        """ HTTP POST Call / get the Server info for upload / timeline.getUploadData
        Args:
            repositoryId (_type_): BPPI Repository ID
        Returns:
            uploadConfig: Upload details configuration
        """
        try: 
            self.log.info("Get the Server info for upload")
            url = self.apiRootPath + C.API_SERVER_UPLOAD_INFOS.format(repositoryId)
            self.log.debug("HTTP POST Request " + url)
            jsondata = json.dumps({"fileName": "timeline.csv"}).encode("utf8")
            self.log.debug("HTTP POST Data sent: ", jsondata)
            req = request.Request(url)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            req.add_header('Authorization', 'Bearer ' + self.Token)
            httpResponse = request.urlopen(req, jsondata).read().decode("utf8")
            cfg = uploadConfig(httpResponse)
            self.log.debug("HTTP Response: {}".format(cfg.jsonContent))
            if (cfg.loaded):
                self.log.info("Upload informations from BPPI collected successfully")
            return cfg
        except Exception as e:
            self.log.error("prepareUpload Error | " + str(e))
            return uploadConfig()

    def uploadData(self, csvData, url, headersAcl) -> bool:
        """HTTP PUT Call / Upload data (csv format) to the server / timeline.uploadFileToS3
        Args:
            csvData (_type_): Data (CSV format)
            url (_type_): BPPI URL (upload destination <- uploadConfig)
            headersAcl (_type_): Header ACL (<- uploadConfig)
        Returns:
            bool: _description_
        """
        try:
            self.log.info("Upload CSV formatted data to the BPPI Server")
            headers = {}
            headers["Authorization"] = "Bearer " + self.Token
            headers["content-type"] = "text/csv"
            headers.update(headersAcl)
            self.log.debug("HTTP PUT Request " + url)
            response = requests.put(url , data=csvData, headers=headers)
            self.log.debug("HTTP Response {}".format(str(response)))
            return response.ok
        except Exception as e:
            self.log.error("uploadData Error | " + str(e))
            return False

    def loadFileToBPPIRepository(self, repositoryId, fkeys, repositoryTable) -> str:
        """ HTTP POST Call / Upload the file in BPPI repo / timeline.loadFileIntoRepositoryTable
        Args:
            repositoryId (_type_): BPPI Repository ID
            fkeys (_type_): Keys
            repositoryTable (_type_): Table to create/append in the Repository
        Returns:
            str: ID of the Process execution
        """
        try:
            self.log.info("Load the file to the BPPI repository")
            url = self.apiRootPath + C.API_SERVER_LOAD_2_REPO.format(repositoryId)
            self.log.debug("HTTP POST Request " + url)
            req = request.Request(url)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            req.add_header('Authorization', 'Bearer ' + self.Token)
            js = {}
            js["fileKeys"] = json.loads(fkeys)
            js["tableName"] = repositoryTable
            jsondata = json.dumps(js).encode("utf8")
            self.log.debug("HTTP POST Data sent: ", jsondata)
            httpResponse = request.urlopen(req, jsondata).read()
            jres2 = json.loads(httpResponse.decode("utf8"))
            self.log.debug("HTTP Response {}".format(jres2))
            self.log.info("Loading the file with process ID {} ".format(jres2["processingId"]))
            return jres2["processingId"]
        except Exception as e:
            self.log.error("loadFileToBPPIRepository Error | " + str(e))
            return str(-1)
    
    def getProcessingStatus(self, processID) -> str:
        """ HTTP Returns the processing Status 
        Args:
            processID (_type_): Process ID
        Raises:
            Exception: Exception / Error with HTTP dump
        Returns:
            str: Status
        """

        try:
            self.log.info("Check status for the BPPI Task {}".format(processID))
            url = self.apiRootPath + C.API_PROCESSING_STATUS + "/" + processID
            self.log.debug("HTTP GET Request " + url)
            response = requests.get(url, headers={ 'Authorization': 'Bearer ' + self.Token, 'content-type': 'application/json' })
            jres = json.loads(response.content)
            self.log.debug("HTTP Response {}".format(response.content))
            self.log.info("BPPI Task {} status is {} ".format(processID, jres["status"]))
            if (jres["status"] == C.API_STATUS_ERROR):
                raise Exception(json.dumps(jres))
            return jres["status"]
        except Exception as e:
            self.log.error("getProcessingStatus Error | " + str(e))
            return C.API_STATUS_ERROR

    def executeTODO(self, repositoryId, todo, tableName) -> str:
        """ HTTPPOST Call / get the Server info for upload / timeline.getUploadData
        Args:
            repositoryId (_type_): Repository ID
            todo (_type_): TO DO Name
            tableName (_type_): Table name
        Returns:
            str: Process ID
        """
        try: 
            self.log.info("Execute a To Do in BPPI repository")
            url = self.apiRootPath + C.API_EXECUTE_TODO.format(repositoryId)
            self.log.debug("HTTP POST Request " + url)
            jsondata = json.dumps({"todoListNames": todo, "tableName" : tableName}).encode("utf8")
            self.log.debug("HTTP POST Data sent: ", jsondata)
            req = request.Request(url)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            req.add_header('Authorization', 'Bearer ' + self.Token)
            httpResponse = request.urlopen(req, jsondata).read()
            jres2 = json.loads(httpResponse.decode("utf8"))
            self.log.debug("HTTP Response {}".format(jres2))
            self.log.info("Loading the file with process ID: " + jres2["processingId"])
            return jres2["processingId"]
        except Exception as e:
            self.log.error(e)
            return str(-1)