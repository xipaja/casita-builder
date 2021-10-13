from .casitaLibrary import CasitaLibrary
from PySide2 import QtWidgets, QtCore, QtGui
import os
from maya import cmds, OpenMayaUI
import pymel.core as pymel
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import pprint

class CasitaUI(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    """
    This is a dialog that allows the user to save and import controllers
    """

    def __init__(self):
            
        super(CasitaUI, self).__init__()

        self.setWindowTitle('Casita Builder')

        # Points to instance of our files library
        self.library = CasitaLibrary()

        # Every time we create a new UI instance, build and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        """
        Build out UI with Qt 
        """

        # Main layout
        layout = QtWidgets.QVBoxLayout(self)
        
        # Gallery of items that can be imported
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(100, 100))

        # Responsive grid UI
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)

        # Buffer space between grid items
        self.listWidget.setGridSize(QtCore.QSize(112, 200))

        layout.addWidget(self.listWidget)
        # Horizontal three buttons layout at the top
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('Import item into scene')
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh items')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)

        # Edit item section - position sliders and color wheel
        editWidget = QtWidgets.QWidget()
        editLayout = QtWidgets.QHBoxLayout(editWidget)
        layout.addWidget(editWidget)

        sliderWidget = QtWidgets.QWidget()
        sliderLayout = QtWidgets.QVBoxLayout(sliderWidget)
        editLayout.addWidget(sliderWidget)

        # Sliders for position of items once loaded
        self.xLabel = QtWidgets.QLabel("X Position")
        self.posLabelX = QtWidgets.QLabel("0")
        sliderLayout.addWidget(self.xLabel)
        sliderLayout.addWidget(self.posLabelX)
        self.xSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.xSlider.setMinimum(-50)
        self.xSlider.setMaximum(50)
        self.xSlider.valueChanged.connect(self.sliderValueChanged)
        sliderLayout.addWidget(self.xSlider)

        self.yLabel = QtWidgets.QLabel("Y Position")
        self.posLabelY = QtWidgets.QLabel("0")
        sliderLayout.addWidget(self.yLabel)
        sliderLayout.addWidget(self.posLabelY)
        self.ySlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.ySlider.setMinimum(-50)
        self.ySlider.setMaximum(50)
        self.ySlider.valueChanged.connect(self.sliderValueChanged)
        sliderLayout.addWidget(self.ySlider)

        self.zLabel = QtWidgets.QLabel("Z Position")
        self.posLabelZ = QtWidgets.QLabel("0")
        sliderLayout.addWidget(self.zLabel)
        sliderLayout.addWidget(self.posLabelZ)
        self.zSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.zSlider.setMinimum(-50)
        self.zSlider.setMaximum(50)
        self.zSlider.valueChanged.connect(self.sliderValueChanged)
        sliderLayout.addWidget(self.zSlider)

        # Color button
        self.colorBtn = QtWidgets.QPushButton()
        self.colorBtn.setFixedSize(100, 70)
        icon = QtGui.QPixmap(os.path.join(cmds.internalVar(userAppDir = True), 'casitaBuilder') + '/color_wheel.PNG')
        self.colorBtn.setIcon(icon)
        self.colorBtn.setIconSize(QtCore.QSize(100, 100))
        self.colorBtn.clicked.connect(self.setColor)
        editLayout.addWidget(self.colorBtn)

        # Save textfield and button layout
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        self.saveTextField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveTextField)

        saveBtn = QtWidgets.QPushButton('Save your casita')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

    def sliderValueChanged(self):
        valueX = self.xSlider.value()
        self.posLabelX.setText(str(valueX))

        valueY = self.ySlider.value()
        self.posLabelY.setText(str(valueY))

        valueZ = self.zSlider.value()
        self.posLabelZ.setText(str(valueZ))
        
        selectedObj = cmds.ls(selection = True)
        if not selectedObj:
            cmds.warning("Select an object in the viewport to move!")

        cmds.move(valueX, valueY, valueZ)        

    def setColor(self):
            # opens up Maya color's editor and we can choose colors there
            color = pymel.colorEditor(rgbValue = (0,1,0))
            selectedObj = cmds.ls(selection = True)[0]
            print("selected", selectedObj)

            # converting our colors to floats to get around Maya's annoying returning colors in string format instead of list
            r, g, b, a = [float(c) for c in color.split()]
            
            # Get material from shading engine so we can change color
            objMesh = cmds.listRelatives(selectedObj, shapes = True)
            objShader = cmds.listConnections(objMesh, type="shadingEngine")[0]
            objMat = cmds.listConnections(objShader + ".surfaceShader")[0]
            
            cmds.setAttr(objMat + ".color", r, g, b)

            objColor = cmds.getAttr(objMat + ".color")
            print("color", objColor)

    def populate(self):
        """
        Clear gallery and repopulate with contents of library
        """
        # Clear out list before finding 
        self.listWidget.clear()

        self.library.find()

        # Add items from info dictionary to gallery
        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            # Create icon for each object with its screenshot
            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)
            
            # Hover over item in grid for info
            item.setToolTip(pprint.pformat(info))

    def load(self):

        currentSelectedItem = self.listWidget.currentItem()

        if not currentSelectedItem:
            cmds.warning("Select an item to import!")
            return

        fileName = currentSelectedItem.text()
        self.library.load(fileName)

    def save(self):
        """
        Saves item with user given file name
        """

        fileName = self.saveTextField.text()
        print("file name", fileName)

        if not fileName.strip():
            cmds.warning("Please enter a file name!")
            return

        self.library.save(fileName)
        self.populate()

        # Set text field string to empty after saving
        self.saveTextField.setText('')

def showUI():
    """
    Shows UI

    Returns: QDialog
    """
    ui = CasitaUI()
    ui.show(dockable = True)
    return ui