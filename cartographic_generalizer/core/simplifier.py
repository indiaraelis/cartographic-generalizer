from qgis.core import QgsGeometry


class Simplifier:
    """
    Implementa algoritmo de simplificação Douglas-Peucker.
    
    Remove vértices desnecessários mantendo a forma essencial da linha.
    """
    
    def simplify(self, geometry, tolerance):
        """
        Simplifica geometria usando Douglas-Peucker.
        
        Args:
            geometry: QgsGeometry a simplificar
            tolerance: tolerância em unidades do mapa (metros normalmente)
        
        Returns:
            QgsGeometry: geometria simplificada
        """
        if geometry.isNull() or geometry.isEmpty():
            return geometry
        
        simplified = geometry.simplify(tolerance)
        
        # Valida resultado
        if simplified.isNull() or simplified.isEmpty():
            return geometry
        
        return simplified

    def adaptive_simplify(self, geometry, ig):
        """
        Simplifica usando tolerância adaptativa baseada em Ig.
        
        Tolerância = Ig * fator_base
        
        Args:
            geometry: QgsGeometry a simplificar
            ig: Índice de Generalização
        
        Returns:
            QgsGeometry: geometria simplificada
        """
        BASE_FACTOR = 10.0
        tolerance = ig * BASE_FACTOR
        
        return self.simplify(geometry, tolerance)
