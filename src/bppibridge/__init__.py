__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import argparse
from pipelines.pipelineFactory import pipelineFactory
from config.cmdLineConfig import cmdLineConfig

def main() -> None:
	"""Entry point for the application script"""
	
	# Get configuration from cmdline & ini file
	config, src = cmdLineConfig.readIni(argparse.ArgumentParser())
	# Process 
	pipelineFactory(src, config).createAndExecute()