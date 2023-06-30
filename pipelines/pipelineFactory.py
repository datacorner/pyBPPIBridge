__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import utils.constants as C
import sys

class pipelineFactory:
	
	@staticmethod
	def create(datasource, config):
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
			sys.path.append(C.PIPELINE_FOLDER)
			if (datasource == C.PARAM_SRCTYPE_VALCSV):
				datasourceObject = __import__("bppiPLRCSVFile").bppiPLRCSVFile
			elif (datasource == C.PARAM_SRCTYPE_VALXES):
				datasourceObject = __import__("bppiPLRXESFile").bppiPLRXESFile
			elif (datasource == C.PARAM_SRCTYPE_VALXLS):
				datasourceObject = __import__("bppiPLRExcelFile").bppiPLRExcelFile
			elif (datasource == C.PARAM_SRCTYPE_VALODBC):
				datasourceObject = __import__("bppiPLRODBC").bppiPLRODBC
			elif (datasource == C.PARAM_SRCTYPE_VALBP):
				datasourceObject = __import__("bppiPLRBluePrismRepo").bppiPLRBluePrismRepo
			elif (datasource == C.PARAM_SRCTYPE_VALBPAPI):
				datasourceObject = __import__("bppiPLRBluePrismApi").bppiPLRBluePrismApi
			elif (datasource == C.PARAM_SRCTYPE_VALSAPTABLE):
				datasourceObject = __import__("bppiPLRSAPRfcTable").bppiPLRSAPRfcTable
			elif (datasource == C.PARAM_SRCTYPE_CHORUSFILE):
				datasourceObject = __import__("bppiPLRChorusExtract").bppiPLRChorusExtract
			else:
				return None
			return datasourceObject(config)
		
		except Exception as e:
			print("Error when loading the Data Source connector: " + str(e))