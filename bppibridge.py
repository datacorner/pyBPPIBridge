__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

from datasources.bppiApiCSVFile import bppiApiCSVFile
from datasources.bppiApiODBC import bppiApiODBC
from datasources.bppiApiBluePrism import bppiApiBluePrism
from datasources.bppiApiExcelFile import bppiApiExcelFile
import argparse
from utils.iniConfig import iniConfig
import constants as C

if __name__ == "__main__":
	# MANAGE CLI ARGUMENTS
	parser = argparse.ArgumentParser()
	try:
		parser.add_argument("-" + C.PARAM_SRCTYPE, help="Data source type {csv|excel|odbc|blueprism}", required=True)
		parser.add_argument("-" + C.PARAM_CONFIGFILE, help="Config file with all configuration details (INI format)", required=True)
		parser.add_argument("-" + C.PARAM_FILENAME, help="(csv) CSV file name and path to import", default=C.EMPTY)
		parser.add_argument("-" + C.PARAM_CSV_SEPARATOR, help="(csv) CSV file field separator (comma by default)", default=C.DEFCSVSEP)
		parser.add_argument("-" + C.PARAM_EXCELSHEETNAME, help="(excel) Excel Sheet name", default="0")
		parser.add_argument("-" + C.PARAM_FROMDATE, help="(blueprism) FROM date -> Delta extraction (Format YYYY-MM-DD HH:MM:SS)", default=C.EMPTY)
		parser.add_argument("-" + C.PARAM_TODATE, help="(blueprism) TO date -> Delta extraction (Format YYYY-MM-DD HH:MM:SS)", default=C.EMPTY)
		args = vars(parser.parse_args())
		config = iniConfig()
		src = args[C.PARAM_SRCTYPE]
		if (not(src in C.PARAM_SRCTYPE_SUPPORTED)):
			raise ("Missing Data Source type {csv|excel|odbc|blueprism}")

		# load configuration via the INI file
		if (args[C.PARAM_CONFIGFILE] != 0):
			config = iniConfig()
			config.loadini(args[C.PARAM_CONFIGFILE])
		else:
			raise ("Missing config file argument {}".format(C.PARAM_CONFIGFILE))
			
		if (src == C.PARAM_SRCTYPE_VALCSV or src == C.PARAM_SRCTYPE_VALXLS):
			# For File (CSV/Excel) load only, takes the CLI args and put them in the config object
			config.addParameter(C.PARAM_FILENAME, args[C.PARAM_FILENAME])
			if (src == C.PARAM_SRCTYPE_VALCSV):
				config.addParameter(C.PARAM_CSV_SEPARATOR, args[C.PARAM_CSV_SEPARATOR])
			if (src == C.PARAM_SRCTYPE_VALXLS):
				config.addParameter(C.PARAM_EXCELSHEETNAME, args[C.PARAM_EXCELSHEETNAME])
			
	except Exception as e:
		print(e)
		parser.print_help()

    # INSTANCIATE THE RIGHT CLASS / DATA SOURCE TYPE
	match args[C.PARAM_SRCTYPE]:
		case C.PARAM_SRCTYPE_VALCSV:
			api = bppiApiCSVFile(config)
		case C.PARAM_SRCTYPE_VALXLS:
			api = bppiApiExcelFile(config)
		case C.PARAM_SRCTYPE_VALODBC:
			api = bppiApiODBC(config)
		case C.PARAM_SRCTYPE_VALBP:
			api = bppiApiBluePrism(config)
		case _:
			parser.print_help()
			exit()
	
    # PROCESS THE DATA
	if (api.initialize()):
		if (src == C.PARAM_SRCTYPE_VALBP or src == C.PARAM_SRCTYPE_VALODBC):
			# Surcharge the Table & To do list parameters / if there's a configuration specified in the INI file
			if (config.getParameter(C.PARAM_BPPITABLE, C.EMPTY) != C.EMPTY):
				api.repositoryConfig.repositoryTableName = config.getParameter(C.PARAM_BPPITABLE)
			if (config.getParameter(C.PARAM_BPPITODOS, C.EMPTY) != C.EMPTY):
				api.repositoryConfig.todoLists = config.getParameter(C.PARAM_BPPITODOS).split(C.DEFCSVSEP)
		df = api.collectData()
		df = api.alterData(df)
		if (df.empty != True):
			if (api.upload(df)):
				api.executeToDo()