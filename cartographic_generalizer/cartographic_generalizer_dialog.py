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
        self.setWindowTitle('Generalização Cartográfica')
        self.setMinimumWidth(500)
        
        layout = QtWidgets.QVBoxLayout()
        
        # Seleção de camada
        group_layer = QtWidgets.QGroupBox('Camada de Entrada')
        layout_layer = QtWidgets.QVBoxLayout()
        
        self.layer_combo = QgsMapLayerComboBox()
        self.layer_combo.setFilters(QgsMapLayerProxyModel.LineLayer)
        layout_layer.addWidget(self.layer_combo)
        
        group_layer.setLayout(layout_layer)
        layout.addWidget(group_layer)
        
        # Escalas
        group_scale = QtWidgets.QGroupBox('Escalas')
        layout_scale = QtWidgets.QFormLayout()
        
        self.scale_origin = QtWidgets.QSpinBox()
        self.scale_origin.setRange(1000, 1000000)
        self.scale_origin.setValue(5000)
        self.scale_origin.setSingleStep(1000)
        
        self.scale_target = QtWidgets.QSpinBox()
        self.scale_target.setRange(1000, 1000000)
        self.scale_target.setValue(25000)
        self.scale_target.setSingleStep(1000)
        
        layout_scale.addRow('Escala Origem (1:)', self.scale_origin)
        layout_scale.addRow('Escala Destino (1:)', self.scale_target)
        
        # Índice de Generalização
        self.ig_label = QtWidgets.QLabel('Ig: -')
        self.ig_label.setStyleSheet('font-weight: bold; color: #2c3e50;')
        layout_scale.addRow('Índice de Generalização:', self.ig_label)
        
        group_scale.setLayout(layout_scale)
        layout.addWidget(group_scale)
        
        # Parâmetros de Generalização
        group_params = QtWidgets.QGroupBox('Parâmetros de Generalização')
        layout_params = QtWidgets.QFormLayout()
        
        # Simplificação
        self.simplify_enabled = QtWidgets.QCheckBox('Ativar Simplificação')
        self.simplify_enabled.setChecked(True)
        layout_params.addRow(self.simplify_enabled)
        
        self.tolerance_spin = QtWidgets.QDoubleSpinBox()
        self.tolerance_spin.setRange(0.1, 1000.0)
        self.tolerance_spin.setValue(10.0)
        self.tolerance_spin.setSingleStep(1.0)
        self.tolerance_spin.setSuffix(' m')
        layout_params.addRow('  Tolerância:', self.tolerance_spin)
        
        # Suavização
        self.smooth_enabled = QtWidgets.QCheckBox('Ativar Suavização')
        self.smooth_enabled.setChecked(True)
        layout_params.addRow(self.smooth_enabled)
        
        self.smooth_iterations = QtWidgets.QSpinBox()
        self.smooth_iterations.setRange(1, 10)
        self.smooth_iterations.setValue(3)
        layout_params.addRow('  Iterações:', self.smooth_iterations)
        
        self.smooth_offset = QtWidgets.QDoubleSpinBox()
        self.smooth_offset.setRange(0.1, 1.0)
        self.smooth_offset.setValue(0.25)
        self.smooth_offset.setSingleStep(0.05)
        layout_params.addRow('  Offset:', self.smooth_offset)
        
        group_params.setLayout(layout_params)
        layout.addWidget(group_params)
        
        # Nome da camada de saída
        group_output = QtWidgets.QGroupBox('Camada de Saída')
        layout_output = QtWidgets.QFormLayout()
        
        self.output_name = QtWidgets.QLineEdit()
        self.output_name.setPlaceholderText('nome_camada_generalizada')
        layout_output.addRow('Nome:', self.output_name)
        
        group_output.setLayout(layout_output)
        layout.addWidget(group_output)
        
        # Botões
        button_box = QtWidgets.QDialogButtonBox()
        self.btn_calculate_ig = QtWidgets.QPushButton('Calcular Ig')
        self.btn_apply = QtWidgets.QPushButton('Aplicar Generalização')
        self.btn_close = QtWidgets.QPushButton('Fechar')
        
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
            default_name = f"{layer.name()}_generalizada_1_{target}"
            self.output_name.setPlaceholderText(default_name)

    def calculate_ig(self):
        origin = self.scale_origin.value()
        target = self.scale_target.value()
        
        ig = self.calculator.calculate_ig(origin, target)
        self.ig_label.setText(f'Ig: {ig:.4f}')
        
        # Sugere tolerância baseada em Ig
        # Lógica: quanto menor Ig, maior a generalização, maior a tolerância
        # Tolerância = (1/Ig) * fator_base
        # Exemplo: Ig = 0.2 → tolerância = (1/0.2) * 10 = 50m
        fator_base = 10.0
        suggested_tolerance = (1 / ig) * fator_base
        self.tolerance_spin.setValue(suggested_tolerance)
        
        QtWidgets.QMessageBox.information(
            self,
            'Índice Calculado',
            f'Índice de Generalização (Ig): {ig:.4f}\n'
            f'(Quanto menor Ig, maior a generalização necessária)\n\n'
            f'Tolerância sugerida: {suggested_tolerance:.2f} m'
        )

    def apply_generalization(self):
        layer = self.layer_combo.currentLayer()
        
        if not layer:
            QtWidgets.QMessageBox.warning(self, 'Aviso', 'Selecione uma camada de entrada')
            return
        
        # Valida geometria
        if layer.geometryType() != QgsWkbTypes.LineGeometry:
            QtWidgets.QMessageBox.warning(self, 'Aviso', 'A camada deve conter geometrias de linha')
            return
        
        # Coleta parâmetros
        params = {
            'simplify': self.simplify_enabled.isChecked(),
            'tolerance': self.tolerance_spin.value(),
            'smooth': self.smooth_enabled.isChecked(),
            'iterations': self.smooth_iterations.value(),
            'offset': self.smooth_offset.value()
        }
        
        # Nome da camada de saída
        output_name = self.output_name.text()
        if not output_name:
            output_name = self.output_name.placeholderText()
        
        # Executa generalização
        try:
            result_layer = self.calculator.generalize_layer(layer, params, output_name)
            
            if result_layer:
                QgsProject.instance().addMapLayer(result_layer)
                
                QtWidgets.QMessageBox.information(
                    self,
                    'Sucesso',
                    f'Camada generalizada criada: {output_name}'
                )
                
                self.accept()
            else:
                QtWidgets.QMessageBox.critical(
                    self,
                    'Erro',
                    'Falha ao criar camada generalizada'
                )
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                'Erro',
                f'Erro ao processar generalização:\n{str(e)}'
            )
