from PySide.QtGui import QWidget, QPushButton, QLabel,\
        QLineEdit, QHBoxLayout, QFormLayout, QVBoxLayout, QMessageBox, QDoubleValidator

from DatabaseManager import Database
from CustomClasses import Designation
from CustomWidgets import ValidatingLineEdit
import mysql.connector
from ShowMySqlError import ShowMysqlError

'''
Add Designation Page
----------------------
We can add new designations to the database from this page
'''

class AddDesignationWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Add Designation"

        self.designation = ValidatingLineEdit("Designation", "[a-zA-Z0-9-_\s]+", self)
        self.da = ValidatingLineEdit("Dearness Allowance", QDoubleValidator(), self)
        self.hra = ValidatingLineEdit("House Rent Allowance", QDoubleValidator(), self)
        self.ta = ValidatingLineEdit("Transport Allowance", QDoubleValidator(), self)
        self.it = ValidatingLineEdit("Income Tax", QDoubleValidator(), self)
        self.pt = ValidatingLineEdit("Professional Tax", QDoubleValidator(), self)

        self.inputs = [self.designation, self.da, self.hra, self.ta, self.it, self.pt]

        self.bttnAddDesignation = QPushButton("Add Designation")
        self.bttnCancel = QPushButton("Cancel")
        self.bttnAddDesignation.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnAddDesignation.clicked.connect(self.add)

        self.setupUI()

    def add(self):
        valid = True

        for i in range(len(self.inputs)):
            if not self.inputs[i].isValid():
                QMessageBox(QMessageBox.Information, "Error", self.inputs[i].getErrorMessage(), parent=self).exec_()
                valid = False
                break
        if valid:
            desg = Designation(self.designation.text(),
                                self.da.text(),
                                self.hra.text(),
                                self.ta.text(),
                                self.it.text(),
                                self.pt.text())
            try:
                Database.getdb().addDesignation(desg)
                QMessageBox(QMessageBox.NoIcon, "Success", "Designation added successfully", parent=self).exec_()
                self.goBack()

            except mysql.connector.Error as e:
                ShowMysqlError(e, self)

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def setupUI(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)
        form = QFormLayout()
        form.setSpacing(20)

        form.addRow(QLabel("Deignation"), self.designation)
        form.addRow(QLabel("Dearness Allowance"), self.da)
        form.addRow(QLabel("House Rent Allowance"), self.hra)
        form.addRow(QLabel("Transport Allowance"), self.ta)
        form.addRow(QLabel("Income Tax"), self.it)
        form.addRow(QLabel("Professional Tax"), self.pt)

        layout.addLayout(form)
        layout.addStretch()
        bttnLayout = QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnCancel)
        bttnLayout.addWidget(self.bttnAddDesignation)


        layout.addLayout(bttnLayout)
        self.setLayout(layout)