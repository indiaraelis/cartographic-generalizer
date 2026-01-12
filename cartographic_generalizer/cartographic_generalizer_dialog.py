from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsProject, QgsVectorLayer, QgsWkbTypes
from qgis.gui import QgsMapLayerComboBox
from qgis.core import QgsMapLayerProxyModel

from .core.generalization_calculator import GeneralizationCalculator


class CartographicGeneralizerDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=None):
        super(CartographicGeneralizerDialog, self).__init__(parent)
        self.calculator = GeneralizationCalculator()
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        self.setWindowTitle('Cartographic Generalization')
        self.setMinimumWidth(500)
        
        layout = QtWidgets.QVBoxLayout()
        
        # Layer selection
        group_layer = QtWidgets.QGroupBox('Input Layer')
        layout_layer = QtWidgets.QVBoxLayout()
        
        self.layer_combo = QgsMapLayerComboBox()
        self.layer_combo.setFilters(QgsMapLayerProxyModel.LineLayer)
        layout_layer.addWidget(self.layer_combo)
        
        group_layer.setLayout(layout_layer)
        layout.addWidget(group_layer)
        
        # Scales
        group_scale = QtWidgets.QGroupBox('Scales')
        layout_scale = QtWidgets.QFormLayout()
        
        self.scale_origin = QtWidgets.QSpinBox()
        self.scale_origin.setRange(1000, 1000000)
        self.scale_origin.setValue(5000)
        self.scale_origin.setSingleStep(1000)
        
        self.scale_target = QtWidgets.QSpinBox()
        self.scale_target.setRange(1000, 1000000)
        self.scale_target.setValue(25000)
        self.scale_target.setSingleStep(1000)
        
        layout_scale.addRow('Origin Scale (1:)', self.scale_origin)
        layout_scale.addRow('Target Scale (1:)', self.scale_target)
        
        # Generalization Index
        self.ig_label = QtWidgets.QLabel('Ig: -')
        self.ig_label.setStyleSheet('font-weight: bold; color: #2c3e50;')
        layout_scale.addRow('Generalization Index:', self.ig_label)
        
        group_scale.setLayout(layout_scale)
        layout.addWidget(group_scale)
        
        # Generalization Parameters
        group_params = QtWidgets.QGroupBox('Generalization Parameters')
        layout_params = QtWidgets.QFormLayout()
        
        # Simplification
        self.simplify_enabled = QtWidgets.QCheckBox('Enable Simplification')
        self.simplify_enabled.setChecked(True)
        layout_params.addRow(self.simplify_enabled)
        
        self.tolerance_spin = QtWidgets.QDoubleSpinBox()
        self.tolerance_spin.setRange(0.1, 1000.0)
        self.tolerance_spin.setValue(10.0)
        self.tolerance_spin.setSingleStep(1.0)
        self.tolerance_spin.setSuffix(' m')
        layout_params.addRow('  Tolerance:', self.tolerance_spin)
        
        # Smoothing
        self.smooth_enabled = QtWidgets.QCheckBox('Enable Smoothing')
        self.smooth_enabled.setChecked(True)
        layout_params.addRow(self.smooth_enabled)
        
        self.smooth_iterations = QtWidgets.QSpinBox()
        self.smooth_iterations.setRange(1, 10)
        self.smooth_iterations.setValue(3)
        layout_params.addRow('  Iterations:', self.smooth_iterations)
        
        self.smooth_offset = QtWidgets.QDoubleSpinBox()
        self.smooth_offset.setRange(0.1, 1.0)
        self.smooth_offset.setValue(0.25)
        self.smooth_offset.setSingleStep(0.05)
        layout_params.addRow('  Offset:', self.smooth_offset)
        
        group_params.setLayout(layout_params)
        layout.addWidget(group_params)
        
        # Output layer name
        group_output = QtWidgets.QGroupBox('Output Layer')
        layout_output = QtWidgets.QFormLayout()
        
        self.output_name = QtWidgets.QLineEdit()
        self.output_name.setPlaceholderText('generalized_layer_name')
        layout_output.addRow('Name:', self.output_name)
        
        group_output.setLayout(layout_output)
        layout.addWidget(group_output)
        
        # Buttons
        button_box = QtWidgets.QDialogButtonBox()
        self.btn_calculate_ig = QtWidgets.QPushButton('Calculate Ig')
        self.btn_apply = QtWidgets.QPushButton('Apply Generalization')
        self.btn_close = QtWidgets.QPushButton('Close')
        
        button_box.addButton(self.btn_calculate_ig, QtWidgets.QDialogButtonBox.ActionRole)
        button_box.addButton(self.btn_apply, QtWidgets.QDialogButtonBox.ActionRole)
        button_box.addButton(self.btn_close, QtWidgets.QDialogButtonBox.RejectRole)
        
        layout.addWidget(button_box)
        
        self.setLayout(layout)

    def connect_signals(self):
        self.btn_calculate_ig.clicked.connect(self.calculate_ig)
        self.btn_apply.clicked.connect(self.apply_generalization)
        self.btn_close.clicked.connect(self.reject)
        
        self.scale_origin.valueChanged.connect(self.update_default_output_name)
        self.scale_target.valueChanged.connect(self.update_default_output_name)
        self.layer_combo.layerChanged.connect(self.update_default_output_name)
        
        self.simplify_enabled.stateChanged.connect(self.toggle_simplify_params)
        self.smooth_enabled.stateChanged.connect(self.toggle_smooth_params)

    def toggle_simplify_params(self):
        enabled = self.simplify_enabled.isChecked()
        self.tolerance_spin.setEnabled(enabled)

    def toggle_smooth_params(self):
        enabled = self.smooth_enabled.isChecked()
        self.smooth_iterations.setEnabled(enabled)
        self.smooth_offset.setEnabled(enabled)

    def update_default_output_name(self):
        layer = self.layer_combo.currentLayer()
        if layer:
            origin = self.scale_origin.value()
            target = self.scale_target.value()
            default_name = f"{layer.name()}_generalized_1_{target}"
            self.output_name.setPlaceholderText(default_name)

    def calculate_ig(self):
        origin = self.scale_origin.value()
        target = self.scale_target.value()
        
        ig = self.calculator.calculate_ig(origin, target)
        self.ig_label.setText(f'Ig: {ig:.4f}')
        
        # Suggest tolerance based on Ig
        # Logic: lower Ig means more generalization, higher tolerance
        # Tolerance = (1/Ig) * base_factor
        # Example: Ig = 0.2 → tolerance = (1/0.2) * 10 = 50m
        fator_base = 10.0
        suggested_tolerance = (1 / ig) * fator_base
        self.tolerance_spin.setValue(suggested_tolerance)
        
        QtWidgets.QMessageBox.information(
            self,
            'Index Calculated',
            f'Generalization Index (Ig): {ig:.4f}\n'
            f'(Lower Ig means more generalization needed)\n\n'
            f'Suggested tolerance: {suggested_tolerance:.2f} m'
        )

    def apply_generalization(self):
        layer = self.layer_combo.currentLayer()
        
        if not layer:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Select an input layer')
            return
        
        # Validate geometry
        if layer.geometryType() != QgsWkbTypes.LineGeometry:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Layer must contain line geometries')
            return
        
        # Collect parameters
        params = {
            'simplify': self.simplify_enabled.isChecked(),
            'tolerance': self.tolerance_spin.value(),
            'smooth': self.smooth_enabled.isChecked(),
            'iterations': self.smooth_iterations.value(),
            'offset': self.smooth_offset.value()
        }
        
        # Output layer name
        output_name = self.output_name.text()
        if not output_name:
            output_name = self.output_name.placeholderText()
        
        # Execute generalization
        try:
            result_layer = self.calculator.generalize_layer(layer, params, output_name)
            
            if result_layer:
                QgsProject.instance().addMapLayer(result_layer)
                
                QtWidgets.QMessageBox.information(
                    self,
                    'Success',
                    f'Generalized layer created: {output_name}'
                )
                
                self.accept()
            else:
                QtWidgets.QMessageBox.critical(
                    self,
                    'Error',
                    'Failed to create generalized layer'
                )
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                'Error',
                f'Error processing generalization:\n{str(e)}'
            )
