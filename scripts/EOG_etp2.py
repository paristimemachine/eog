from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsFeature,
    QgsField,
    QgsFeatureSink
)
from PyQt5.QtCore import QVariant
import statistics

class TypologyClassifierDynamic(QgsProcessingAlgorithm):
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('INPUT_LAYER', 'Couche vectorielle avec sélection'))
        self.addParameter(QgsProcessingParameterNumber('THRESHOLD', 'Seuil de typologie (écart normalisé moyen)',
                                                       type=QgsProcessingParameterNumber.Double, defaultValue=2.0))
        self.addParameter(QgsProcessingParameterFeatureSink('OUTPUT_LAYER', 'Couche typologisée'))

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, 'INPUT_LAYER', context)
        threshold = self.parameterAsDouble(parameters, 'THRESHOLD', context)

        stat_fields = ['meanB0', 'meanB1', 'meanB2', 'varB0', 'varB1', 'varB2']
        selected_features = input_layer.selectedFeatures()
        if not selected_features:
            raise Exception("Aucune entité sélectionnée dans la couche.")

        stats = {}
        for field in stat_fields:
            values = [f[field] for f in selected_features if f[field] is not None]
            stats[field] = {
                'mean': statistics.mean(values),
                'stdev': statistics.stdev(values) if len(values) > 1 else 1e-6
            }

        fields = input_layer.fields()
        fields.append(QgsField('typologie', QVariant.Int))

        (sink, dest_id) = self.parameterAsSink(parameters, 'OUTPUT_LAYER', context,
                                               fields, input_layer.wkbType(), input_layer.sourceCrs())

        for feature in input_layer.getFeatures():
            score = 0
            count = 0
            for field in stat_fields:
                value = feature[field]
                if value is None:
                    continue
                mean = stats[field]['mean']
                stdev = stats[field]['stdev']
                score += abs(value - mean) / stdev
                count += 1
            avg_score = score / count if count > 0 else float('inf')
            typology = 1 if avg_score <= threshold else 2

            if typology == 1:
                new_feature = QgsFeature()
                new_feature.setGeometry(feature.geometry())
                attrs = feature.attributes()
                attrs.append(typology)
                new_feature.setAttributes(attrs)
                sink.addFeature(new_feature, QgsFeatureSink.FastInsert)

        return {'OUTPUT_LAYER': dest_id}

    def name(self):
        return 'typology_classifier_dynamic'

    def displayName(self):
        return 'Typologie dynamique par moyenne des écarts normalisés'

    def group(self):
        return 'Étape 2'
        return 'Classification OTB'

    def groupId(self):
        return 'etape_2'
        return 'classification_otb'

    def createInstance(self):
        return TypologyClassifierDynamic()
