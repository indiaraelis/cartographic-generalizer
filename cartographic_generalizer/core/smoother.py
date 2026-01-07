from qgis.core import QgsGeometry


class Smoother:
    """
    Implementa algoritmo de suavização Chaikin.
    
    Reduz ângulos agudos nos segmentos de linha mantendo forma geral.
    """
    
    def smooth(self, geometry, iterations=3, offset=0.25):
        """
        Suaviza geometria usando algoritmo Chaikin.
        
        Args:
            geometry: QgsGeometry a suavizar
            iterations: número de iterações (quanto maior, mais suave)
            offset: deslocamento dos pontos (0.25 = padrão Chaikin)
        
        Returns:
            QgsGeometry: geometria suavizada
        """
        if geometry.isNull() or geometry.isEmpty():
            return geometry
        
        smoothed = geometry.smooth(iterations, offset)
        
        # Valida resultado
        if smoothed.isNull() or smoothed.isEmpty():
            return geometry
        
        return smoothed

    def conservative_smooth(self, geometry, max_iterations=2):
        """
        Aplica suavização conservadora (menos agressiva).
        
        Args:
            geometry: QgsGeometry a suavizar
            max_iterations: número máximo de iterações
        
        Returns:
            QgsGeometry: geometria suavizada
        """
        return self.smooth(geometry, iterations=max_iterations, offset=0.2)

    def aggressive_smooth(self, geometry, max_iterations=5):
        """
        Aplica suavização agressiva (mais suave).
        
        Args:
            geometry: QgsGeometry a suavizar
            max_iterations: número máximo de iterações
        
        Returns:
            QgsGeometry: geometria suavizada
        """
        return self.smooth(geometry, iterations=max_iterations, offset=0.3)
