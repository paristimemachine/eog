# -*- coding: utf-8 -*-
from qgis.core import (
    QgsProcessing, QgsProcessingAlgorithm,
    QgsProcessingParameterRasterLayer, QgsProcessingParameterFileDestination,
    QgsProcessingException
)
from qgis import processing
import os
import tempfile

class OTB_LargeScaleMeanShift(QgsProcessingAlgorithm):
    RASTER = 'RASTER'
    VECTOR_OUT = 'VECTOR_OUT'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            self.RASTER, 'Raster d’entrée'))
        self.addParameter(QgsProcessingParameterFileDestination(
            self.VECTOR_OUT, 'Shapefile vectorisé (sortie)',
            fileFilter='ESRI Shapefile (*.shp)'))

    def processAlgorithm(self, parameters, context, feedback):
        raster = self.parameterAsRasterLayer(parameters, self.RASTER, context)
        vector_out = self.parameterAsFileOutput(parameters, self.VECTOR_OUT, context)

        if raster is None:
            raise QgsProcessingException('Raster d’entrée manquant.')

        # Fichier temporaire pour la sortie raster obligatoire
        temp_raster_out = os.path.join(tempfile.gettempdir(), 'lsms_temp_raster.tif')

        feedback.pushInfo('LargeScaleMeanShift…')
        result = processing.run('otb:LargeScaleMeanShift', {
            'in': raster.source(),
            'spatialr': 5,
            'ranger': 15,
            'minsize': 0,
            'tilesizex': 500,
            'tilesizey': 500,
            'mode': 'vector',
            'mode.vector.out': vector_out,
            'mode.raster.out': temp_raster_out
        }, context=context, feedback=feedback)

        feedback.pushInfo('OK : {}'.format(result['mode.vector.out']))
        return { self.VECTOR_OUT: result['mode.vector.out'] }

    def name(self): return 'otb_largescale_meanshift'
    def displayName(self): return 'OTB — LargeScaleMeanShift (tout-en-un)'
    def group(self):
        return 'Étape 1'
    def groupId(self):
        return 'etape_1'
    def createInstance(self): return OTB_LargeScaleMeanShift()
