from DatabaseManager import Database
from PySide import QtGui
from PySide.QtCore import Qt


class ShowEmployeeWidget(QtGui.QWidget):
    """PySide widget that shows all the employee informations in a tabular form

    QTableWidget is used to show the info in a table. The ``getAllEmployeeInfo()`` method from DatabaseManager is
    used to get all the information as a list which is then arranged in the QTableWidget.

    See Also:
        - :py:meth:`getAllEmployeeInfo() <DatabaseManager.databaseManager.DatabaseManager.getAllEmployeeInfo>` method of DatabaseManager

    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Show Employee"

        self.table = QtGui.QTableWidget(self)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.loadTable()

        self.bttnBack = QtGui.QPushButton("Back")
        self.bttnBack.clicked.connect(self.goBack)
        self.bttnBack.setObjectName("CancelButton")

        self.setupUI()

    def loadTable(self):
        """Loads all the info in the QTableWidget"""

        info = Database.getdb().getAllEmployeeInfo()
        self.table.setRowCount(len(info))
        self.table.setColumnCount(len(info[0]))

        for i in range(len(info)):
            for j in range(len(info[0])):
                self.table.setItem(i, j, QtGui.QTableWidgetItem(str(info[i][j])))

        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Designation", "Original Pay", "Original Pay Grade", "DOJ", "PAN"])
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, Qt.AscendingOrder)

    def setupUI(self):
        """Arranges GUI elements inside the widget properly"""
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
