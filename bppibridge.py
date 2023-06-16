__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import argparse
from utils.iniConfig import iniConfig
import constants as C

try:
	from datasources.bppiDSCSVFile import bppiDSCSVFile
	from datasources.bppiDSODBC import bppiDSODBC
	from datasources.bppiDSBluePrism import bppiDSBluePrism
	from datasources.bppiDSExcelFile import bppiDSExcelFile
	from datasources.bppiDSSAPRfcTable import bppiDSSAPRfcTable
	from datasources.bppiDSXESFile import bppiDSXESFile
	_MODULE_LOADED_ = True
except Exception as e:
	_MODULE_LOADED_ = False
	print("Error when loading some/all pyBPPIBridge Data Sources Connectors" + str(e))

if __name__ == "__main__":
	# MANAGE CLI ARGUMENTS
	parser = argparse.ArgumentParser()
	try:
		parser.add_argument("-" + C.PARAM_SRCTYPE, help="Data source type {csv|xes|excel|odbc|blueprism|saptable}", required=True)
		parser.add_argument("-" + C.PARAM_CONFIGFILE, help="Config file with all configuration details (INI format)", required=True)
		parser.add_argument("-" + C.PARAM_FILENAME, help="(csv|xes|excel) File name and path to import", default=C.EMPTY)
		parser.add_argument("-" + C.PARAM_CSV_SEPARATOR, help="(csv) CSV file field separator (comma by default)", default=C.DEFCSVSEP)
		parser.add_argument("-" + C.PARAM_EXCELSHEETNAME, help="(excel) Excel Sheet name", default="0")
		parser.add_argument("-" + C.PARAM_FROMDATE, help="(blueprism) FROM date -> Delta extraction (Format YYYY-MM-DD HH:MM:SS)", default=C.EMPTY)
		parser.add_argument("-" + C.PARAM_TODATE, help="(blueprism) TO date -> Delta extraction (Format YYYY-MM-DD HH:MM:SS)", default=C.EMPTY)
		args = vars(parser.parse_args())
		config = iniConfig()
		src = args[C.PARAM_SRCTYPE]
		if (not(src in C.PARAM_SRCTYPE_SUPPORTED)):
			raise Exception("Missing Data Source type {csv|xes|excel|odbc|blueprism|saptable}")

		# load configuration via the INI file
		if (args[C.PARAM_CONFIGFILE] != 0):
			config.loadini(args[C.PARAM_CONFIGFILE])
		else:
			raise Exception("Missing config file argument {}".format(C.PARAM_CONFIGFILE))
			
		if (src == C.PARAM_SRCTYPE_VALCSV or src == C.PARAM_SRCTYPE_VALXLS or src == C.PARAM_SRCTYPE_VALXES):
			# For File (CSV/XES/Excel) load only, takes the CLI args and put them in the config object
			config.addParameter(C.PARAM_FILENAME, args[C.PARAM_FILENAME])
			if (src == C.PARAM_SRCTYPE_VALCSV):
				config.addParameter(C.PARAM_CSV_SEPARATOR, args[C.PARAM_CSV_SEPARATOR])
			if (src == C.PARAM_SRCTYPE_VALXLS):
				config.addParameter(C.PARAM_EXCELSHEETNAME, args[C.PARAM_EXCELSHEETNAME])
	
	except Exception as e:
		print(e)
		parser.print_help()
		exit()

    # INSTANCIATE THE RIGHT CLASS / DATA SOURCE TYPE
	match args[C.PARAM_SRCTYPE]:
		case C.PARAM_SRCTYPE_VALCSV:
			job = bppiDSCSVFile(config)
		case C.PARAM_SRCTYPE_VALXES:
			job = bppiDSXESFile(config)
		case C.PARAM_SRCTYPE_VALXLS:
			job = bppiDSExcelFile(config)
		case C.PARAM_SRCTYPE_VALODBC:
			job = bppiDSODBC(config)
		case C.PARAM_SRCTYPE_VALBP:
			job = bppiDSBluePrism(config)
		case C.PARAM_SRCTYPE_VALSAPTABLE:
			job = bppiDSSAPRfcTable(config)
		case _:
			parser.print_help()
			exit()
	
    # PROCESS THE DATA
	if (job.initialize()):
		if (src == C.PARAM_SRCTYPE_VALBP or src == C.PARAM_SRCTYPE_VALODBC):
			# Surcharge the Table & To do list parameters / if there's a configuration specified in the INI file
			if (config.getParameter(C.PARAM_BPPITABLE, C.EMPTY) != C.EMPTY):
				job.repositoryConfig.repositoryTableName = config.getParameter(C.PARAM_BPPITABLE)
			if (config.getParameter(C.PARAM_BPPITODOS, C.EMPTY) != C.EMPTY):
				job.repositoryConfig.todoLists = config.getParameter(C.PARAM_BPPITODOS).split(C.DEFCSVSEP)
		df = job.collectData()
		if (df.shape[0] == 0):
			job.log.info("There are no data to manage, terminate here.")
		else:
			df = job.alterData(df)
			if (df.empty != True):
				if (job.upload(df) and config.getParameter(C.PARAM_BPPITODOACTIVED, C.NO) == C.YES):
					job.executeToDo()
		job.terminate()