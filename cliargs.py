__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import constants as C
from utils.iniConfig import iniConfig

def cliargs(parser):
	""" This function gather the arguments sent in the CLI and build the configuration object.
    Args:
        parser (argparse.ArgumentParser): CLI arguments
    Raises:
        Exception: Unable to gather the CLI args
    Returns:
        utils.iniConfig: config object
		string: Data Source Tag (command line)
	"""
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
		return config, src

	except Exception as e:
		print(e)
		parser.print_help()
		return None, None