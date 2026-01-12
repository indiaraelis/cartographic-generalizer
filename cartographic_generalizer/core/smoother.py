from qgis.core import QgsGeometry


class Smoother:
    """
    Implements Chaikin smoothing algorithm.
    
    Reduces sharp angles in line segments while maintaining general shape.
    """
    
    def smooth(self, geometry, iterations=3, offset=0.25):
        """
        Smooths geometry using Chaikin algorithm.
        
        Args:
            geometry: QgsGeometry to smooth
            iterations: number of iterations (higher = smoother)
            offset: point displacement (0.25 = classic Chaikin)
        
        Returns:
            QgsGeometry: smoothed geometry
        """
        if geometry.isNull() or geometry.isEmpty():
            return geometry
        
        smoothed = geometry.smooth(iterations, offset)
        
        # Validate result
        if smoothed.isNull() or smoothed.isEmpty():
            return geometry
        
        return smoothed

    def conservative_smooth(self, geometry, max_iterations=2):
        """
        Applies conservative smoothing (less aggressive).
        
        Args:
            geometry: QgsGeometry to smooth
            max_iterations: maximum number of iterations
        
        Returns:
            QgsGeometry: smoothed geometry
        """
        return self.smooth(geometry, iterations=max_iterations, offset=0.2)

    def aggressive_smooth(self, geometry, max_iterations=5):
        """
        Applies aggressive smoothing (smoother result).
        
        Args:
            geometry: QgsGeometry to smooth
            max_iterations: maximum number of iterations
        
        Returns:
            QgsGeometry: smoothed geometry
        """
        return self.smooth(geometry, iterations=max_iterations, offset=0.3)
