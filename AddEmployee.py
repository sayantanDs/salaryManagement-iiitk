from PySide import QtGui, QtCore

from CustomWidgets import DatePicker
from DatabaseManager import Database

import mysql.connector
from ShowMySqlError import ShowMysqlError
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

        self.id = QtGui.QLineEdit(self)
        self.id.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z0-9-_]+")))
        self.name = QtGui.QLineEdit(self)
        self.name.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z\s]+")))
        self.designation = QtGui.QComboBox(self)

        # self.designation.addItems(Database.getdb().getDesignations())

        self.originalPay = QtGui.QLineEdit(self)
        self.originalPay.setValidator(QtGui.QDoubleValidator())
        self.originalPayGrade = QtGui.QLineEdit(self)
        self.originalPayGrade.setValidator(QtGui.QDoubleValidator())
        self.DOJ = DatePicker(self)
        self.pan = QtGui.QLineEdit(self)
        self.pan.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Z]{5}\d{4}[A-Z]")))

        self.bttnAddEmployee = QtGui.QPushButton("Add Employee")
        self.bttnCancel = QtGui.QPushButton("Cancel")
        self.bttnAddEmployee.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnAddEmployee.clicked.connect(self.add)

        self.designation.addItems(Database.getdb().getDesignations())

        self.setupUI()

    def add(self):
        id = self.id.text()
        name = self.name.text()
        designation = self.designation.currentText()
        originalPay = self.originalPay.text()
        originalPayGrade = self.originalPayGrade.text()
        doj = self.DOJ.getDate()
        pan = self.pan.text()

        if "" in [id, name, designation, originalPay, originalPayGrade, doj, pan]:
            msg = QtGui.QMessageBox(QtGui.QMessageBox.Information, "Error", "Please enter all the information!", parent=self)
            msg.exec_()
        else:
            doj = "%4d-%02d-%02d" % (doj.year(), doj.month(), doj.day())
            print id, name, designation, originalPay, originalPayGrade, doj, pan

            try:
                Database.getdb().addEmployee(id, name, designation, float(originalPay), float(originalPayGrade), doj, pan)
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