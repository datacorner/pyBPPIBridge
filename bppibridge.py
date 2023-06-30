__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import argparse
import utils.constants as C
from pipelines.pipelineFactory import pipelineFactory
from configuration import configuration

if __name__ == "__main__":
	# MANAGE CLI ARGUMENTS --> Build Config Object
	config, src = configuration.fromCmdLine(argparse.ArgumentParser())
	if (config == None): exit()

    # INSTANCIATE ONLY THE NEEDED CLASS / DATA SOURCE TYPE
	pipeline = pipelineFactory.create(src, config)

    # PROCESS THE DATA
	if (pipeline.initialize()):
		df = pipeline.extract()	# EXTRACT (E of ETL)
		if (df.shape[0] == 0):
			pipeline.log.info("There are no data to process, terminate here.")
		else:
			df = pipeline.transform(df)	# TRANSFORM (T of ETL)
			if (df.empty != True): 
				# LOAD (L of ETL)
				if (pipeline.load(df) and config.getParameter(C.PARAM_BPPITODOACTIVED, C.NO) == C.YES):
					pipeline.executeToDo()
		pipeline.terminate()