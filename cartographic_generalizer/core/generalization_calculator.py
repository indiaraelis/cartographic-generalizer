from qgis.core import (
    QgsVectorLayer, 
    QgsFeature, 
    QgsGeometry,
    QgsWkbTypes
)

from .simplifier import Simplifier
from .smoother import Smoother


class GeneralizationCalculator:
    
    def __init__(self):
        self.simplifier = Simplifier()
        self.smoother = Smoother()

    def calculate_ig(self, scale_origin, scale_target):
        """
        Calculates the Generalization Index (Ig) based on scale change.
        
        Formula: Ig = Do/Dg (according to Dal Santo, 2007)
        Where Do = origin scale denominator, Dg = target scale denominator
        
        Example: 1:5,000 -> 1:25,000 results in Ig = 5000/25000 = 0.2
        
        Interpretation: Ig < 1 indicates generalization is needed.
        Lower Ig means more generalization.
        
        Args:
            scale_origin: Origin scale denominator (e.g., 5000)
            scale_target: Target scale denominator (e.g., 25000)
        
        Returns:
            float: Generalization Index (0 < Ig < 1 for generalization)
        
        References:
            Dal Santo, M.A. (2007). Generalização cartográfica automatizada 
            para um banco de dados cadastral. PhD Thesis - UFSC.
        """
        if scale_origin <= 0 or scale_target <= 0:
            raise ValueError("Scales must be greater than zero")
        
        if scale_target <= scale_origin:
            raise ValueError("Target scale must be smaller than origin (larger denominator)")
        
        # Correct formula according to thesis: Ig = Do/Dg
        ig = scale_origin / scale_target
        return ig

    def generalize_layer(self, input_layer, params, output_name):
        """
        Applies cartographic generalization to a layer.
        
        Args:
            input_layer: Input QgsVectorLayer
            params: dict with generalization parameters
            output_name: output layer name
        
        Returns:
            QgsVectorLayer: generalized layer or None if error
        """
        if not input_layer or not input_layer.isValid():
            return None
        
        # Create output layer
        output_layer = QgsVectorLayer(
            f"{QgsWkbTypes.displayString(input_layer.wkbType())}?crs={input_layer.crs().authid()}",
            output_name,
            "memory"
        )
        
        provider = output_layer.dataProvider()
        
        # Copy fields
        provider.addAttributes(input_layer.fields())
        output_layer.updateFields()
        
        # Process each feature
        features = input_layer.getFeatures()
        generalized_features = []
        
        for feature in features:
            geom = feature.geometry()
            
            if geom.isNull() or geom.isEmpty():
                continue
            
            # Apply simplification
            if params.get('simplify', False):
                tolerance = params.get('tolerance', 10.0)
                geom = self.simplifier.simplify(geom, tolerance)
            
            # Apply smoothing
            if params.get('smooth', False):
                iterations = params.get('iterations', 3)
                offset = params.get('offset', 0.25)
                geom = self.smoother.smooth(geom, iterations, offset)
            
            # Create new feature
            new_feature = QgsFeature()
            new_feature.setGeometry(geom)
            new_feature.setAttributes(feature.attributes())
            generalized_features.append(new_feature)
        
        # Add generalized features
        provider.addFeatures(generalized_features)
        output_layer.updateExtents()
        
        return output_layer

    def calculate_sinuosity(self, geometry):
        """
        Calculates the sinuosity of a line.
        
        Sinuosity = real_length / euclidean_distance
        
        Args:
            geometry: Line QgsGeometry
        
        Returns:
            float: índice de sinuosidade (1.0 = linha reta)
        """
        if geometry.isNull() or geometry.isEmpty():
            return 1.0
        
        real_length = geometry.length()
        
        # Pega primeiro e último ponto
        vertices = geometry.asPolyline()
        if len(vertices) < 2:
            return 1.0
        
        first_point = vertices[0]
        last_point = vertices[-1]
        
        euclidean_distance = first_point.distance(last_point)
        
        if euclidean_distance == 0:
            return 1.0
        
        sinuosity = real_length / euclidean_distance
        return sinuosity
