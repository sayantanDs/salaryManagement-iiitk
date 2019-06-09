from DatabaseManager import Database
from PySide import QtGui
from CustomWidgets import SearchBox


class DelEmployeeWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DelEmployeeWidget, self).__init__(parent)
        self.__parent = parent
        self.title = "Delete Employee"
        self.idList = []

        nameList = Database.getdb().getEmployeeNameList()
        self.name = SearchBox(self, nameList)
        self.name.setPlaceholderText("Enter Name")

        self.name.returnPressed.connect(self.setIdList)

        self.id = QtGui.QComboBox()
        self.id.currentIndexChanged.connect(lambda: self.updateInformation(self.id.currentText()))

        self.designation = QtGui.QLineEdit()
        self.designation.setReadOnly(True)
        self.joinDate = QtGui.QLineEdit()
        self.joinDate.setReadOnly(True)
        self.panNo = QtGui.QLineEdit()
        self.panNo.setReadOnly(True)

        self.remove = QtGui.QPushButton("Remove Employee")
        self.remove.clicked.connect(self.removeEmployee)
        self.remove.setObjectName("CancelButton")

        self.back = QtGui.QPushButton("Back")
        self.back.clicked.connect(self.goBack)
        self.back.setObjectName("OkButton")

        self.setupUI()

    def loadNameList(self):
        self.name = SearchBox(self, Database.getdb().getEmployeeNameList())


    def setIdList(self, name):
        self.id.clear()
        self.id.addItems(Database.getdb().getIdListForName(name))

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def updateInformation(self, id):

        emp = Database.getdb().getEmployeeInfo(id)
        if emp is None:
            self.designation.clear()
            self.joinDate.clear()
            self.panNo.clear()
        else:
            self.designation.setText(emp.designation)
            self.joinDate.setText(emp.getStrDate())
            self.panNo.setText(emp.pan)

    def setupUI(self):

        paneLayout = QtGui.QHBoxLayout()
        paneLayout.setContentsMargins(0, 0, 0, 0)

        leftPane = QtGui.QFrame()
        leftPane.setObjectName("leftPane")

        leftPaneLayout = QtGui.QVBoxLayout()
        leftPaneLayout.setContentsMargins(20, 20, 20, 10)
        heading = QtGui.QLabel("Select Employee: ")
        heading.setObjectName("heading")
        leftPaneLayout.addWidget(heading)
        leftPaneLayout.addSpacing(10)

        leftForm = QtGui.QFormLayout()
        leftForm.addRow(QtGui.QLabel("Name"), self.name)
        leftForm.addRow(QtGui.QLabel("Employee ID"), self.id)
        leftPaneLayout.addLayout(leftForm)
        leftPaneLayout.addStretch()
        leftPane.setLayout(leftPaneLayout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)

        infoGroup = QtGui.QGroupBox("Basic Info:")
        formLayout = QtGui.QFormLayout()
        formLayout.setContentsMargins(10, 10, 10, 30)
        formLayout.setSpacing(20)

        # formLayout.addRow(QtGui.QLabel("Name"), self.name)
        # formLayout.addRow(QtGui.QLabel("Employee ID"), self.id)
        formLayout.addRow(QtGui.QLabel("Designation"), self.designation)
        formLayout.addRow(QtGui.QLabel("Date of join"), self.joinDate)
        formLayout.addRow(QtGui.QLabel("Pan No"), self.panNo)


        infoGroup.setLayout(formLayout)


        mainLayout.addWidget(infoGroup)
        mainLayout.addStretch()

        bttnLayout = QtGui.QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.back)
        bttnLayout.addWidget(self.remove)
        mainLayout.addLayout(bttnLayout)

        paneLayout.addWidget(leftPane)
        paneLayout.addLayout(mainLayout)
        self.setLayout(paneLayout)

    def removeEmployee(self):

        if str(self.id.currentText()) == "":
            msg = QtGui.QMessageBox(QtGui.QMessageBox.Information, "Error!!!", "First enter all the information", parent=self)
            msg.exec_()
        else:
            choice = QtGui.QMessageBox.question(self, 'Remove Confirmation!!!',
                                                "Are you sure you want to delete this employee?\nName: " + str(
                                                    self.name.text()) + "\nID: " +
                                                    self.id.currentText() + "\nDesignation: " + str(
                                                    self.designation.text()),
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:
                try:
                    Database.getdb().delEmployee(self.id.currentText())
                    msg = QtGui.QMessageBox(QtGui.QMessageBox.NoIcon, "Success", "Deleted Successfully", parent=self)
                    msg.exec_()
                    # reload name list
                    self.name.clear()
                    nameList = Database.getdb().getEmployeeNameList()
                    self.name.addItems(nameList)
                    self.name.setCurrentIndex(-1)

                except Exception as e:
                    raise e

