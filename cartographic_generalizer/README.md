# Cartographic Generalizer

QGIS plugin for cartographic generalization of linear features based on scale change.

## Description

This plugin implements automatic cartographic generalization using the Generalization Index (Ig) derived from scale changes. It applies simplification (Douglas-Peucker) and smoothing (Chaikin) operators to linear features such as contour lines, rivers, and other line geometries.

Based on cartographic generalization concepts from Dal Santo, M.A. (2007) thesis on automated cartographic generalization for cadastral databases.

## Features

- **Generalization Index (Ig) Calculation**: automatically calculated based on origin/target scale
- **Simplification**: removes unnecessary vertices using Douglas-Peucker algorithm
- **Smoothing**: reduces sharp angles using Chaikin algorithm
- **Simple Interface**: all parameters in a single window
- **Manual Control**: user defines all parameters

## Installation

### Method 1: Via Plugin Manager (when published)

1. Open QGIS
2. Menu `Plugins > Manage and Install Plugins`
3. Search for "Cartographic Generalizer"
4. Click `Install Plugin`

### Method 2: Manual Installation

1. Locate QGIS plugins folder:
   - **Windows**: `C:\Users\YOUR_USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
   - **Mac**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`

2. Copy the `cartographic_generalizer` folder to the plugins directory

3. Restart QGIS

4. Enable the plugin in `Plugins > Manage and Install Plugins > Installed`

## Usage

1. Open a vector line layer (contour lines, hydrography, etc.)

2. Access the plugin:
   - Menu: `Vector > Cartographic Generalizer > Cartographic Generalization`
   - Or click the toolbar icon

3. Configure parameters:
   - **Input Layer**: select the layer to generalize
   - **Origin Scale**: original data scale (e.g., 5000 for 1:5,000)
   - **Target Scale**: desired scale (e.g., 25000 for 1:25,000)
   - Click **Calculate Ig** to see the index and suggested tolerance

4. Adjust generalization parameters:
   - **Simplification**: 
     - Check to enable
     - Adjust tolerance (m) - higher values mean more simplification
   - **Smoothing**:
     - Check to enable
     - Adjust iterations (1-10) - higher values mean smoother lines
     - Adjust offset (0.1-1.0) - controls intensity

5. Define output layer name

6. Click **Apply Generalization**

## Concepts

### Generalization Index (Ig)

**Formula:** Ig = Do/Dg (according to Dal Santo, 2007)

Where:
- Do = denominator of origin scale
- Dg = denominator of generalized scale (target)

Example: 1:5,000 → 1:25,000 results in Ig = 5000/25000 = 0.2

**Interpretation:**
- Ig < 1 indicates need for generalization
- Lower Ig values mean more generalization is needed
- Ig = 0.2 means the scale is 5x smaller (less detailed)

### Simplification (Douglas-Peucker)

Removes vertices while maintaining essential shape. Tolerance defines maximum allowed distance between original and simplified line.

### Smoothing (Chaikin)

Reduces sharp angles creating smoother curves. Each iteration smooths the line further.

## Usage Examples

### Contour Lines

- **Origin Scale**: 5000 (1:5,000)
- **Target Scale**: 25000 (1:25,000)
- **Ig**: 0.2 (5000/25000)
- **Simplification**: Enabled, tolerance ~2.5m (automatically suggested)
- **Smoothing**: Enabled, 3 iterations, offset 0.25

### Rivers/Hydrography

- **Origin Scale**: 10000 (1:10,000)
- **Target Scale**: 50000 (1:50,000)
- **Ig**: 0.2 (10000/50000)
- **Simplification**: Enabled, tolerance ~2.5m (automatically suggested)
- **Smoothing**: Enabled, 3 iterations, offset 0.25

**Note**: Tolerance values are automatically calculated using the formula (1/Ig) × 0.5, resulting in appropriate values for the scale change. Adjust as needed for your specific data.

## Requirements

- QGIS 3.0 or higher
- Python 3.6+
- PyQt5 (included with QGIS)

## Limitations

- Processes only line geometries (LineString)
- Does not consider network hierarchy (Strahler order)
- Does not automatically preserve connectivity between features
- Processes one layer at a time

## Future Development

Possible improvements:

- Support for Strahler order for hydrography
- Automatic connectivity preservation
- Batch processing of multiple layers
- Saved parameter presets
- Statistics report (vertices removed, etc.)

## Author

Developed by Indiara Elis.

## License

GPL v3 or later

## Contributing

Contributions are welcome! Open issues or pull requests in the repository.

## References

Based on cartographic generalization concepts from:

- DAL SANTO, M. A. Generalização cartográfica automatizada para um banco de dados cadastral. 2007. PhD Thesis - Federal University of Santa Catarina, Florianópolis, 2007. Available at: http://repositorio.ufsc.br/xmlui/handle/123456789/89592
- McMaster, R. B., & Shea, K. S. (1992). Generalization in Digital Cartography
- Keates, J. S. (1989). Cartographic Design and Production
