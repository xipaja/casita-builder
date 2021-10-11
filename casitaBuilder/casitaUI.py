from .casitaLibrary import CasitaLibrary
from PySide2 import QtWidgets, QtCore, QtGui

class CasitaUI(QtWidgets.QDialog):
    """
    This is a dialog that allows the user to save and import controllers
    """

    def __init__(self):
        super(CasitaUI, self).__init__()

        self.setWindowTitle('Casita Builder')

        # Store instance of our files ilbrary in theUI
        self.library = CasitaLibrary()

        # Every time we create a new UI instance, build and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('Import into scene')
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
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

        saveBtn = QtWidgets.QPushButton('Save as ma file')
        saveLayout.addWidget(saveBtn)


    def populate(self):
        self.library.find()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            # Create icon for each object with its screenshot
            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)


def showUI():
    ui = CasitaUI()
    ui.show()
    return ui