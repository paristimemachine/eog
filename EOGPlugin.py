from qgis.core import QgsProcessingProvider
from .scripts.EOG_etp1 import OTB_LargeScaleMeanShift
from .scripts.EOG_etp2 import TypologyClassifierDynamic
from .scripts.EOG_etp3 import DataCleaningWithSimplificationAndSmoothing

class EOGProvider(QgsProcessingProvider):
    def loadAlgorithms(self):
        self.addAlgorithm(OTB_LargeScaleMeanShift())
        self.addAlgorithm(TypologyClassifierDynamic())
        self.addAlgorithm(DataCleaningWithSimplificationAndSmoothing())

    def id(self):
        return "eog"

    def name(self):
        return "EOG"

    def longName(self):
        return "Extraction d'objets géographiques"

class EOGPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.provider = EOGProvider()

    def initGui(self):
        from qgis.core import QgsApplication
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        from qgis.core import QgsApplication
        QgsApplication.processingRegistry().removeProvider(self.provider)
