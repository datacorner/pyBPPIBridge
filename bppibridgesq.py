__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import argparse
from pipelines.pipelineFactory import pipelineFactory
from config.configuration import configuration

if __name__ == "__main__":
	# Get configuration from cmdline & ini file
	config, src = configuration.fromCmdLine_sqlite(argparse.ArgumentParser())
	# Process 
	pipelineFactory(src, config).createAndExecute()