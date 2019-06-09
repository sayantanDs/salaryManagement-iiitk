from PySide import QtGui, QtCore
from CustomWidgets import DatePicker
from DatabaseManager import Database
import mysql.connector
from ShowMySqlError import ShowMysqlError
from CustomWidgets import ValidatingLineEdit
from CustomClasses import Employee


'''
Add Employee Page
-------------------
We can add new employees to the database from this page
'''
class AddEmployeeWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Add Employee"

        self.id = ValidatingLineEdit("ID", "[a-zA-Z0-9-_]+", self)
        self.name = ValidatingLineEdit("Name", "[a-zA-Z\s]+", self)
        self.designation = QtGui.QComboBox(self)
        self.designation.addItems(Database.getdb().getDesignations())
        self.originalPay = ValidatingLineEdit("Original Pay", QtGui.QDoubleValidator(), self)
        self.originalPayGrade = ValidatingLineEdit("Original Pay Grade", QtGui.QDoubleValidator(), self)
        self.DOJ = DatePicker(self)
        self.pan = ValidatingLineEdit("PAN", "[A-Z]{5}\d{4}[A-Z]", self)

        self.inputs = [self.id, self.name, self.originalPay, self.originalPayGrade, self.pan]

        self.bttnAddEmployee = QtGui.QPushButton("Add Employee")
        self.bttnCancel = QtGui.QPushButton("Cancel")
        self.bttnAddEmployee.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnAddEmployee.clicked.connect(self.add)

        # self.designation.addItems(Database.getdb().getDesignations())

        self.setupUI()

    def add(self):
        valid = True
        for i in range(len(self.inputs)):
            if not self.inputs[i].isValid():
                valid = False
                QtGui.QMessageBox(QtGui.QMessageBox.Information, "Error", self.inputs[i].getErrorMessage(),
                                        parent=self).exec_()
                break

        if valid:
            emp = Employee(self.id.text(),
                           self.name.text(),
                           self.designation.currentText(),
                           self.originalPay.text(),
                           self.originalPayGrade.text(),
                           self.DOJ.getDate(),
                           self.pan.text())
            try:
                Database.getdb().addEmployee(emp)
            except mysql.connector.Error as e:
                ShowMysqlError(e, self)
                return

            QtGui.QMessageBox(QtGui.QMessageBox.NoIcon, "Success", "Employee added successfully", parent=self).exec_()

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def setupUI(self):
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)
        form = QtGui.QFormLayout()
        form.setSpacing(20)
        form.addRow(QtGui.QLabel("ID No."), self.id)
        form.addRow(QtGui.QLabel("Name"), self.name)
        form.addRow(QtGui.QLabel("Designation"), self.designation)
        form.addRow(QtGui.QLabel("Original Pay"), self.originalPay)
        form.addRow(QtGui.QLabel("Original Pay Grade"), self.originalPayGrade)
        form.addRow(QtGui.QLabel("Date of joining"), self.DOJ)
        form.addRow(QtGui.QLabel("Pan No."), self.pan)
        layout.addLayout(form)
        layout.addStretch()
        bttnLayout = QtGui.QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnCancel)
        bttnLayout.addWidget(self.bttnAddEmployee)

        layout.addLayout(bttnLayout)
        self.setLayout(layout)