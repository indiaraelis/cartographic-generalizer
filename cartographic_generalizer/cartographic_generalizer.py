import os
from qgis.PyQt.QtCore import QCoreApplication, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject

from .cartographic_generalizer_dialog import CartographicGeneralizerDialog


class CartographicGeneralizer:
    
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = '&Cartographic Generalizer'
        self.toolbar = self.iface.addToolBar('CartographicGeneralizer')
        self.toolbar.setObjectName('CartographicGeneralizer')
        self.dlg = None

    def add_action(self, icon_path, text, callback, enabled_flag=True, 
                   add_to_menu=True, add_to_toolbar=True, status_tip=None, 
                   whats_this=None, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        
        if status_tip is not None:
            action.setStatusTip(status_tip)
        
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        
        if add_to_toolbar:
            self.toolbar.addAction(action)
        
        if add_to_menu:
            self.iface.addPluginToVectorMenu(self.menu, action)
        
        self.actions.append(action)
        return action

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.add_action(
            icon_path,
            text='Generalização Cartográfica',
            callback=self.run,
            parent=self.iface.mainWindow()
        )

    def unload(self):
        for action in self.actions:
            self.iface.removePluginVectorMenu('&Cartographic Generalizer', action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        if self.dlg is None:
            self.dlg = CartographicGeneralizerDialog()
        
        self.dlg.show()
        result = self.dlg.exec_()
        
        if result:
            pass
