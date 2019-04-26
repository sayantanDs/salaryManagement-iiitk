from PySide.QtGui import QWidget, QPushButton, QLabel,\
        QLineEdit, QComboBox, QHBoxLayout, QFormLayout, QVBoxLayout, QMessageBox, QDoubleValidator, QRegExpValidator

from PySide.QtCore import QRegExp

from CustomWidgets import DatePicker
import DatabaseManager

import mysql.connector
from ShowMySqlError import ShowMysqlError
'''
Add Employee Page
-------------------
We can add new employees to the database from this page
'''

class AddEmployeeWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Add Employee"

        self.id = QLineEdit(self)
        self.id.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9-_]+")))
        self.name = QLineEdit(self)
        self.name.setValidator(QRegExpValidator(QRegExp("[a-zA-Z\s]+")))
        self.designation = QComboBox(self)

        # self.designation.addItems(DatabaseManager.db.getDesignations())

        self.originalPay = QLineEdit(self)
        self.originalPay.setValidator(QDoubleValidator())
        self.originalPayGrade = QLineEdit(self)
        self.originalPayGrade.setValidator(QDoubleValidator())
        self.DOJ = DatePicker(self)
        self.pan = QLineEdit(self)
        self.pan.setValidator(QRegExpValidator(QRegExp("[A-Z]{5}\d{4}[A-Z]")))

        self.bttnAddEmployee = QPushButton("Add Employee")
        self.bttnCancel = QPushButton("Cancel")
        self.bttnAddEmployee.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnAddEmployee.clicked.connect(self.add)

        self.designation.addItems(DatabaseManager.db.getDesignations())

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
            msg = QMessageBox(QMessageBox.Information, "Error", "Please enter all the information!", parent=self)
            msg.exec_()
        else:
            doj = "%4d-%02d-%02d" % (doj.year(), doj.month(), doj.day())
            print id, name, designation, originalPay, originalPayGrade, doj, pan

            try:
                DatabaseManager.db.addEmployee(id, name, designation, float(originalPay), float(originalPayGrade), doj, pan)
            except mysql.connector.Error as e:
                ShowMysqlError(e, self)
                return

            QMessageBox(QMessageBox.NoIcon, "Success", "Employee added successfully", parent=self).exec_()


    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def setupUI(self):
        # self.bttnAddEmployee.setMinimumSize(100, 30)
        # self.bttnCancel.setMinimumSize(100, 30)
        # self.id.setMaximumWidth(800)
        # self.name.setMaximumWidth(800)
        # self.designation.setMaximumWidth(800)
        # self.originalPay.setMaximumWidth(800)
        # self.originalPayGrade.setMaximumWidth(800)
        # self.DOJ.setMaximumWidth(800)
        # self.pan.setMaximumWidth(800)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)
        form = QFormLayout()
        form.setSpacing(20)
        form.addRow(QLabel("ID No."), self.id)
        form.addRow(QLabel("Name"), self.name)
        form.addRow(QLabel("Designation"), self.designation)
        form.addRow(QLabel("Original Pay"), self.originalPay)
        form.addRow(QLabel("Original Pay Grade"), self.originalPayGrade)
        form.addRow(QLabel("Date of joining"), self.DOJ)
        form.addRow(QLabel("Pan No."), self.pan)
        layout.addLayout(form)
        layout.addStretch()
        bttnLayout = QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnCancel)
        bttnLayout.addWidget(self.bttnAddEmployee)

        layout.addLayout(bttnLayout)
        self.setLayout(layout)