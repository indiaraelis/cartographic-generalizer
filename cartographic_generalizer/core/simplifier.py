from qgis.core import QgsGeometry


class Simplifier:
    """
    Implements Douglas-Peucker simplification algorithm.
    
    Removes unnecessary vertices while maintaining essential line shape.
    """
    
    def simplify(self, geometry, tolerance):
        """
        Simplifies geometry using Douglas-Peucker.
        
        Args:
            geometry: QgsGeometry to simplify
            tolerance: tolerance in map units (usually meters)
        
        Returns:
            QgsGeometry: simplified geometry
        """
        if geometry.isNull() or geometry.isEmpty():
            return geometry
        
        simplified = geometry.simplify(tolerance)
        
        # Validate result
        if simplified.isNull() or simplified.isEmpty():
            return geometry
        
        return simplified

    def adaptive_simplify(self, geometry, ig):
        """
        Simplifies using adaptive tolerance based on Ig.
        
        Tolerance = Ig * base_factor
        
        Args:
            geometry: QgsGeometry to simplify
            ig: Generalization Index
        
        Returns:
            QgsGeometry: simplified geometry
        """
        BASE_FACTOR = 10.0
        tolerance = ig * BASE_FACTOR
        
        return self.simplify(geometry, tolerance)
