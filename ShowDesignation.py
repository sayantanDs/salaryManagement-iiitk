from DatabaseManager import Database
from PySide import QtGui
from PySide.QtCore import Qt


class ShowDesigationWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Show Designation"

        self.table = QtGui.QTableWidget(self)

        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.loadTable()

        self.bttnBack = QtGui.QPushButton("Back")
        self.bttnBack.clicked.connect(self.goBack)
        self.bttnBack.setObjectName("CancelButton")


        self.setupUI()

    def loadTable(self):

        info = Database.getdb().getAllDesignationInfo()
        self.table.setRowCount(len(info))
        self.table.setColumnCount(len(info[0]))

        for i in range(len(info)):
            for j in range(len(info[0])):
                self.table.setItem(i, j, QtGui.QTableWidgetItem(str(info[i][j])))

        self.table.setHorizontalHeaderLabels(
            ["Designation", "DA", "HRA", "TA", "IT", "PT"])
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, Qt.AscendingOrder)

    def setupUI(self):
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)

        layout.addWidget(self.table)

        layout.addSpacing(50)
        bttnLayout = QtGui.QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnBack)

        layout.addLayout(bttnLayout)
        self.setLayout(layout)


    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()
