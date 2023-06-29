__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import constants as C
from utils.appConfig import appConfig

class configuration:
	
	@staticmethod
	def fromDB(id):
		pass

	@staticmethod
	def fromCmdLine(parser):
		""" This function gather the arguments sent in the CLI and build the configuration object.
		Args:
			parser (argparse.ArgumentParser): CLI arguments
		Raises:
			Exception: Unable to gather the CLI args
		Returns:
			utils.appConfig: config object
			string: Data Source Tag (command line)
		"""
		try:
			config = appConfig()

			# Parser CLI arguments
			parser.add_argument("-" + C.PARAM_SRCTYPE, help="(All) Data source type {csv|xes|excel|odbc|bprepo|bpapi|saptable}", required=True)
			parser.add_argument("-" + C.PARAM_CONFIGFILE, help="(All) Config file with all configuration details (INI format)", required=True)
			parser.add_argument("-" + C.PARAM_FILENAME, help="(csv|xes|excel) File name and path to import", default=C.EMPTY)
			parser.add_argument("-" + C.PARAM_CSV_SEPARATOR, help="(csv) CSV file field separator (comma by default)", default=C.DEFCSVSEP)
			parser.add_argument("-" + C.PARAM_EXCELSHEETNAME, help="(excel) Excel Sheet name", default="0")
			parser.add_argument("-" + C.PARAM_FROMDATE, help="(bprepo) FROM date -> Delta extraction (Format YYYY-MM-DD HH:MM:SS)", default=C.EMPTY)
			parser.add_argument("-" + C.PARAM_TODATE, help="(bprepo) TO date -> Delta extraction (Format YYYY-MM-DD HH:MM:SS)", default=C.EMPTY)
			args = vars(parser.parse_args())
			# Check Data Source Type
			src = args[C.PARAM_SRCTYPE]
			if (not(src in C.PARAM_SRCTYPE_SUPPORTED)):
				raise Exception("Missing Data Source type {csv|xes|excel|odbc|bprepo|bpapi|saptable}")
			# Load configuration via the INI file
			if (args[C.PARAM_CONFIGFILE] != 0):
				config.loadFromINIFile(args[C.PARAM_CONFIGFILE])
			else:
				raise Exception("Missing config file argument {}".format(C.PARAM_CONFIGFILE))
			# Config "exceptions" ...
			file_management = (src == C.PARAM_SRCTYPE_VALCSV or 
							src == C.PARAM_SRCTYPE_VALXLS or 
							src == C.PARAM_SRCTYPE_VALXES or 
							src == C.PARAM_SRCTYPE_CHORUSFILE)
			if (file_management):
				# For File (CSV/XES/Excel) load only, takes the CLI args and put them in the config object
				config.addParameter(C.PARAM_FILENAME, args[C.PARAM_FILENAME])
				if (src == C.PARAM_SRCTYPE_VALCSV or src == C.PARAM_SRCTYPE_CHORUSFILE):
					config.addParameter(C.PARAM_CSV_SEPARATOR, args[C.PARAM_CSV_SEPARATOR])
				if (src == C.PARAM_SRCTYPE_VALXLS):
					config.addParameter(C.PARAM_EXCELSHEETNAME, args[C.PARAM_EXCELSHEETNAME])
			return config, src

		except Exception as e:
			print(e)
			parser.print_help()
			return None, None