from .casitaLibrary import CasitaLibrary
from PySide2 import QtWidgets, QtCore, QtGui
from maya import cmds
import pymel.core as pymel
import pprint

class CasitaUI(QtWidgets.QDialog):
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
        xLabel = QtWidgets.QLabel("X Position")
        xSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        xSlider.setMinimum(-100)
        xSlider.setMaximum(100)
        xSlider.setGeometry(0, 0, 50, 30)
        sliderLayout.addWidget(xLabel)
        sliderLayout.addWidget(xSlider)
        yLabel = QtWidgets.QLabel("Y Position")
        sliderLayout.addWidget(yLabel)
        ySlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        ySlider.setGeometry(0, 0, 50, 30)
        sliderLayout.addWidget(ySlider)
        zLabel = QtWidgets.QLabel("Z Position")
        sliderLayout.addWidget(zLabel)
        zSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        zSlider.setGeometry(0, 0, 50, 30)
        sliderLayout.addWidget(zSlider)

        # Color button
        self.colorBtn = QtWidgets.QPushButton()
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

    def setColor(self):
            # opens up Maya color's editor and we can choose colors there
            color = pymel.colorEditor(rgbValue = (0,1,0))

            # converting our colors to floats to get around Maya's annoying returning colors in string format instead of list
            r, g, b, a = [float(c) for c in color.split()]
            
            color = (r, g, b)

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
            cmds.warning("You must select an item to import!")
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
            cmds.warning("You must give a file name!")
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
    ui.show()
    return ui