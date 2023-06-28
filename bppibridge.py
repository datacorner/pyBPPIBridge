__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import argparse
import constants as C
from pipeline import createPipeline
from cliargs import cliargs

if __name__ == "__main__":
	# MANAGE CLI ARGUMENTS --> Build Config Object
	config, src = cliargs(argparse.ArgumentParser())
	if (config == None): exit()

    # INSTANCIATE ONLY THE NEEDED CLASS / DATA SOURCE TYPE
	pipeline = createPipeline(src, config)

    # PROCESS THE DATA
	if (pipeline.initialize()):
		if (src == C.PARAM_SRCTYPE_VALBP or src == C.PARAM_SRCTYPE_VALODBC):
			# Surcharge the Table & To do list parameters / if there's a configuration specified in the INI file
			if (config.getParameter(C.PARAM_BPPITABLE, C.EMPTY) != C.EMPTY):
				pipeline.repositoryConfig.repositoryTableName = config.getParameter(C.PARAM_BPPITABLE)
			if (config.getParameter(C.PARAM_BPPITODOS, C.EMPTY) != C.EMPTY):
				pipeline.repositoryConfig.todoLists = config.getParameter(C.PARAM_BPPITODOS).split(C.DEFCSVSEP)
		df = pipeline.extract()	# EXTRACT (E of ETL)
		if (df.shape[0] == 0):
			pipeline.log.info("There are no data to manage, terminate here.")
		else:
			df = pipeline.transform(df)	# TRANSFORM (T of ETL)
			if (df.empty != True): 
				# LOAD (L of ETL)
				if (pipeline.load(df) and config.getParameter(C.PARAM_BPPITODOACTIVED, C.NO) == C.YES):
					pipeline.executeToDo()
		pipeline.terminate()