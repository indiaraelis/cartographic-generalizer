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
        Calcula o Índice de Generalização (Ig) baseado na mudança de escala.
        
        Fórmula: Ig = Do/Dg (conforme Dal Santo, 2007)
        Onde Do = denominador escala origem, Dg = denominador escala destino
        
        Exemplo: 1:5.000 -> 1:25.000 resulta em Ig = 5000/25000 = 0.2
        
        Interpretação: Ig < 1 indica generalização necessária.
        Quanto menor o Ig, maior a generalização.
        
        Args:
            scale_origin: Denominador da escala de origem (ex: 5000)
            scale_target: Denominador da escala de destino (ex: 25000)
        
        Returns:
            float: Índice de Generalização (0 < Ig < 1 para generalização)
        
        References:
            Dal Santo, M.A. (2007). Generalização cartográfica automatizada 
            para um banco de dados cadastral. Tese (Doutorado) - UFSC.
        """
        if scale_origin <= 0 or scale_target <= 0:
            raise ValueError("Escalas devem ser maiores que zero")
        
        if scale_target <= scale_origin:
            raise ValueError("Escala de destino deve ser menor que origem (denominador maior)")
        
        # Fórmula correta conforme tese: Ig = Do/Dg
        ig = scale_origin / scale_target
        return ig

    def generalize_layer(self, input_layer, params, output_name):
        """
        Aplica generalização cartográfica em uma camada.
        
        Args:
            input_layer: QgsVectorLayer de entrada
            params: dict com parâmetros de generalização
            output_name: nome da camada de saída
        
        Returns:
            QgsVectorLayer: camada generalizada ou None se erro
        """
        if not input_layer or not input_layer.isValid():
            return None
        
        # Cria camada de saída
        output_layer = QgsVectorLayer(
            f"{QgsWkbTypes.displayString(input_layer.wkbType())}?crs={input_layer.crs().authid()}",
            output_name,
            "memory"
        )
        
        provider = output_layer.dataProvider()
        
        # Copia campos
        provider.addAttributes(input_layer.fields())
        output_layer.updateFields()
        
        # Processa cada feição
        features = input_layer.getFeatures()
        generalized_features = []
        
        for feature in features:
            geom = feature.geometry()
            
            if geom.isNull() or geom.isEmpty():
                continue
            
            # Aplica simplificação
            if params.get('simplify', False):
                tolerance = params.get('tolerance', 10.0)
                geom = self.simplifier.simplify(geom, tolerance)
            
            # Aplica suavização
            if params.get('smooth', False):
                iterations = params.get('iterations', 3)
                offset = params.get('offset', 0.25)
                geom = self.smoother.smooth(geom, iterations, offset)
            
            # Cria nova feição
            new_feature = QgsFeature()
            new_feature.setGeometry(geom)
            new_feature.setAttributes(feature.attributes())
            generalized_features.append(new_feature)
        
        # Adiciona feições generalizadas
        provider.addFeatures(generalized_features)
        output_layer.updateExtents()
        
        return output_layer

    def calculate_sinuosity(self, geometry):
        """
        Calcula a sinuosidade de uma linha.
        
        Sinuosidade = comprimento_real / distância_euclidiana
        
        Args:
            geometry: QgsGeometry de linha
        
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
