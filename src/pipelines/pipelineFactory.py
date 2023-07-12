__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import utils.constants as C
import sys
import os
import importlib

class pipelineFactory:
	def __init__(self, datasource, config):
		self.__config = config
		self.__datasource = datasource
    
	@property
	def config(self):
		return self.__config
	@property
	def datasource(self):
		return self.__datasource
	
	def createAndExecute(self):
		# INSTANCIATE ONLY THE NEEDED CLASS / DATA SOURCE TYPE
		pipeline = self.create()
		if (pipeline == None): exit()
		# PROCESS THE DATA
		if (pipeline.initialize()):
			df = pipeline.extract()	# EXTRACT (E of ETL)
			if (df.shape[0] == 0):
				pipeline.log.info("There are no data to process, terminate here.")
			else:
				df = pipeline.transform(df)	# TRANSFORM (T of ETL)
				if (df.empty != True): 
					# LOAD (L of ETL)
					if (pipeline.load(df) and self.config.getParameter(C.PARAM_BPPITODOACTIVED, C.NO) == C.YES):
						pipeline.executeToDo()
			pipeline.terminate()

	def create(self):
		""" This function dynamically instanciate the right data pipeline (manages ETL) class to create a pipeline object. 
			This to avoid in loading all the connectors (if any of them failed for example) when making a global import, 
			by this way only the needed import is done on the fly
			Args:
				pipeline (str): Datasource type
				config (config): Configuration set
			Returns:
				Object: Data Source Object
		"""
		try:
			if (self.config == None): 
				raise Exception("The configuration is not available or is invalid.")
			if (self.datasource == None): 
				raise Exception("The datasource is not correctly specified or is invalid.")
			if (self.datasource == C.PARAM_SRCTYPE_VALCSV):
				datasourceObject = importlib.import_module(C.PIPELINE_FOLDER + "bppiPLRCSVFile").bppiPLRCSVFile
			elif (self.datasource == C.PARAM_SRCTYPE_VALXES):
				datasourceObject = __import__(C.PIPELINE_FOLDER + "bppiPLRXESFile").bppiPLRXESFile
			elif (self.datasource == C.PARAM_SRCTYPE_VALXLS):
				datasourceObject = __import__(C.PIPELINE_FOLDER + "bppiPLRExcelFile").bppiPLRExcelFile
			elif (self.datasource == C.PARAM_SRCTYPE_VALODBC):
				datasourceObject = __import__(C.PIPELINE_FOLDER + "bppiPLRODBC").bppiPLRODBC
			elif (self.datasource == C.PARAM_SRCTYPE_VALBP):
				datasourceObject = __import__(C.PIPELINE_FOLDER + "bppiPLRBluePrismRepo").bppiPLRBluePrismRepo
			elif (self.datasource == C.PARAM_SRCTYPE_VALBPAPI):
				datasourceObject = __import__(C.PIPELINE_FOLDER + "bppiPLRBluePrismApi").bppiPLRBluePrismApi
			elif (self.datasource == C.PARAM_SRCTYPE_VALSAPTABLE):
				datasourceObject = __import__(C.PIPELINE_FOLDER + "bppiPLRSAPRfcTable").bppiPLRSAPRfcTable
			elif (self.datasource == C.PARAM_SRCTYPE_CHORUSFILE):
				datasourceObject = __import__(C.PIPELINE_FOLDER + "bppiPLRChorusExtract").bppiPLRChorusExtract
			else:
				raise Exception ("Error when loading the Data Source Factory in pipeline folder")
			return datasourceObject(self.config)
		
		except Exception as e:
			print("Error when loading the Data Source Factory: " + str(e))
			return None