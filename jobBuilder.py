__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import constants as C
import sys

def jobBuilder(datasource, config):
	""" This function dynamically instanciate the right datasource class to create the job object. 
		... This to avoid in loading all the connectors (if any of them failed for example)
		Args:
			datasource (_type_): Datasource type
			config (_type_): Configuration set
		Returns:
			Object: Data Source Object
	"""
	try:
		sys.path.append('datasources')
		if (datasource == C.PARAM_SRCTYPE_VALCSV):
			datasourceObject = __import__("bppiDSCSVFile").bppiDSCSVFile
		elif (datasource == C.PARAM_SRCTYPE_VALXES):
			datasourceObject = __import__("bppiDSXESFile").bppiDSXESFile
		elif (datasource == C.PARAM_SRCTYPE_VALXLS):
			datasourceObject = __import__("bppiDSExcelFile").bppiDSExcelFile
		elif (datasource == C.PARAM_SRCTYPE_VALODBC):
			datasourceObject = __import__("bppiDSODBC").bppiDSODBC
		elif (datasource == C.PARAM_SRCTYPE_VALBP):
			datasourceObject = __import__("bppiDSBluePrism").bppiDSBluePrism
		elif (datasource == C.PARAM_SRCTYPE_VALSAPTABLE):
			datasourceObject = __import__("bppiDSSAPRfcTable").bppiDSSAPRfcTable
		else:
			return None
		
		return datasourceObject(config)
	except Exception as e:
		print("Error when loading the Data Source connector: " + str(e))