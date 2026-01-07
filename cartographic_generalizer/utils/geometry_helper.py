from qgis.core import QgsGeometry, QgsPointXY


class GeometryHelper:
    """
    Funções auxiliares para manipulação de geometrias.
    """
    
    @staticmethod
    def calculate_length(geometry):
        """
        Calcula comprimento de linha.
        
        Args:
            geometry: QgsGeometry
        
        Returns:
            float: comprimento em unidades do mapa
        """
        if geometry.isNull() or geometry.isEmpty():
            return 0.0
        
        return geometry.length()
    
    @staticmethod
    def calculate_euclidean_distance(geometry):
        """
        Calcula distância euclidiana entre primeiro e último ponto.
        
        Args:
            geometry: QgsGeometry de linha
        
        Returns:
            float: distância euclidiana
        """
        if geometry.isNull() or geometry.isEmpty():
            return 0.0
        
        vertices = geometry.asPolyline()
        if len(vertices) < 2:
            return 0.0
        
        first = vertices[0]
        last = vertices[-1]
        
        return first.distance(last)
    
    @staticmethod
    def get_vertex_count(geometry):
        """
        Conta número de vértices em geometria.
        
        Args:
            geometry: QgsGeometry
        
        Returns:
            int: número de vértices
        """
        if geometry.isNull() or geometry.isEmpty():
            return 0
        
        vertices = geometry.asPolyline()
        return len(vertices)
    
    @staticmethod
    def is_closed_line(geometry):
        """
        Verifica se linha é fechada (primeiro = último ponto).
        
        Args:
            geometry: QgsGeometry de linha
        
        Returns:
            bool: True se fechada
        """
        if geometry.isNull() or geometry.isEmpty():
            return False
        
        vertices = geometry.asPolyline()
        if len(vertices) < 2:
            return False
        
        first = vertices[0]
        last = vertices[-1]
        
        return first == last
