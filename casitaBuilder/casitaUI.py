from .casitaLibrary import CasitaLibrary
from PySide2 import QtWidgets, QtCore, QtGui
from maya import cmds

class CasitaUI(QtWidgets.QDialog):
    """
    This is a dialog that allows the user to save and import controllers
    """

    def __init__(self):
        super(CasitaUI, self).__init__()

        self.setWindowTitle('Casita Builder')

        # Store instance of our files library in theUI
        self.library = CasitaLibrary()

        # Every time we create a new UI instance, build and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

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

        # Gallery of items that can be imported
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(100, 100))

        # Responsive grid UI
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)

        # Buffer space between grid items
        self.listWidget.setGridSize(QtCore.QSize(112, 200))

        layout.addWidget(self.listWidget)

        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        self.saveTextField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveTextField)

        saveBtn = QtWidgets.QPushButton('Save your casita')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)


    def populate(self):
        # Clear out list before finding 
        self.listWidget.clear()

        self.library.find()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            # Create icon for each object with its screenshot
            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

    def load(self):

        currentSelectedItem = self.listWidget.currentItem()

        if not currentSelectedItem:
            cmds.warning("You must select an item to import!")
            return

        fileName = currentSelectedItem.text()
        self.library.load(fileName)

    def save(self):

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
    ui = CasitaUI()
    ui.show()
    return ui