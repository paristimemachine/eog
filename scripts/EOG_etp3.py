from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber
)
from qgis import processing

class DataCleaningWithSimplificationAndSmoothing(QgsProcessingAlgorithm):
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('INPUT_LAYER', 'Couche vectorielle à nettoyer'))
        self.addParameter(QgsProcessingParameterNumber('TOLERANCE', 'Tolérance de simplification (mètres)',
                                                       type=QgsProcessingParameterNumber.Double, defaultValue=0.5))
        self.addParameter(QgsProcessingParameterNumber('ITERATIONS', 'Nombre d’itérations de lissage',
                                                       type=QgsProcessingParameterNumber.Integer, defaultValue=3))
        self.addParameter(QgsProcessingParameterNumber('OFFSET', 'Décalage de lissage',
                                                       type=QgsProcessingParameterNumber.Double, defaultValue=0.25))
        self.addParameter(QgsProcessingParameterFeatureSink('OUTPUT_LAYER', 'Couche nettoyée'))

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, 'INPUT_LAYER', context)
        tolerance = self.parameterAsDouble(parameters, 'TOLERANCE', context)
        iterations = self.parameterAsInt(parameters, 'ITERATIONS', context)
        offset = self.parameterAsDouble(parameters, 'OFFSET', context)

        feedback.pushInfo("Réparation des géométries...")
        repair_result = processing.run("native:fixgeometries", {
            'INPUT': input_layer,
            'OUTPUT': 'memory:'
        }, context=context)

        feedback.pushInfo("Fusion des polygones...")
        dissolve_result = processing.run("native:dissolve", {
            'INPUT': repair_result['OUTPUT'],
            'OUTPUT': 'memory:'
        }, context=context)

        feedback.pushInfo("Éclatement des multipolygones...")
        explode_result = processing.run("native:multiparttosingleparts", {
            'INPUT': dissolve_result['OUTPUT'],
            'OUTPUT': 'memory:'
        }, context=context)

        feedback.pushInfo("Suppression des trous < 20 m²...")
        remove_holes_result = processing.run("native:deleteholes", {
            'INPUT': explode_result['OUTPUT'],
            'MIN_AREA': 20,
            'OUTPUT': 'memory:'
        }, context=context)

        feedback.pushInfo("Simplification géométrique (topologie préservée)...")
        simplify_result = processing.run("native:simplifygeometries", {
            'INPUT': remove_holes_result['OUTPUT'],
            'METHOD': 1,  # Topology-preserving
            'TOLERANCE': tolerance,
            'OUTPUT': 'memory:'
        }, context=context)

        feedback.pushInfo("Lissage des géométries...")
        smooth_result = processing.run("native:smoothgeometry", {
            'INPUT': simplify_result['OUTPUT'],
            'ITERATIONS': iterations,
            'OFFSET': offset,
            'MAX_ANGLE': 180,
            'OUTPUT': parameters['OUTPUT_LAYER']
        }, context=context)

        return {'OUTPUT_LAYER': smooth_result['OUTPUT']}

    def name(self):
        return 'data_cleaning_with_simplification_and_smoothing'

    def displayName(self):
        return 'Nettoyage complet avec simplification et lissage'

    def group(self):
        return 'Étape 3'
        return 'Traitements personnalisés'

    def groupId(self):
        return 'etape_3'
        return 'traitements_perso'

    def createInstance(self):
        return DataCleaningWithSimplificationAndSmoothing()
