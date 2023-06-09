__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

from bppiapi.repository.bppiApiRepositoryWrapper import bppiApiRepositoryWrapper
from bppiapi.bppiPipeline import bppiPipeline
import utils.constants as C

MANDATORY_PARAM_LIST = [C.PARAM_BPPITOKEN, 
                        C.PARAM_BPPIURL]

class bppiProject(bppiPipeline):
    def __init__(self, config):
        super().__init__(config)
        self.__projectInfos = None   # BPPI Project infos (gathered from the bppi server)
