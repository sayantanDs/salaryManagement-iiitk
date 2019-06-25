import sys

from PySide import QtGui, QtCore
from PySide.QtGui import QWidget, QApplication, QPushButton, QLabel,\
        QLineEdit, QComboBox, QHBoxLayout, QFormLayout, QVBoxLayout, QMessageBox, QFrame, QFileDialog, QSpinBox, QGroupBox
from printPaySlip import printPaySlip
from CustomClasses import Salary, Employee
from DatabaseManager import Database
import mysql.connector
from mysql.connector import errorcode
from ShowMySqlError import ShowMysqlError

class ShowPaySlipWidget(QWidget):
    """Shows the calculated salary for confirmation"""
    def __init__(self, parent, salary):
        QWidget.__init__(self)
        self.title = "Salary Result"
        # self.setGeometry(50, 50, 800, 600)

        self.__parent = parent
        self.salary = salary

        self.month = str(self.salary.month)
        self.year = str(self.salary.year)
        self.id = QLineEdit()
        self.id.setReadOnly(True)
        self.id.setText(self.salary.id)
        self.name = QLineEdit()
        self.name.setReadOnly(True)
        self.name.setText(self.salary.name)
        self.designation = QLineEdit()
        self.designation.setReadOnly(True)
        self.designation.setText(self.salary.designation)
        self.originalPay = QLineEdit()
        self.originalPay.setReadOnly(True)
        self.originalPay.setText(str(self.salary.originalPay))
        self.originalPayGrade = QLineEdit()
        self.originalPayGrade.setReadOnly(True)
        self.originalPayGrade.setText(str(self.salary.originalPayGrade))
        self.DOJ = QLineEdit()
        self.DOJ.setReadOnly(True)
        self.DOJ.setText(Employee.dateToStr(salary.doj))
        self.pan = QLineEdit()
        self.pan.setReadOnly(True)
        self.pan.setText(self.salary.pan)

        self.presentPay = QLineEdit()
        self.presentPay.setReadOnly(True)
        self.presentPay.setText(str(self.salary.presentPay))
        self.da = QLineEdit()
        self.da.setReadOnly(True)
        self.da.setText(str(self.salary.da))
        self.hra = QLineEdit()
        self.hra.setReadOnly(True)
        self.hra.setText(str(self.salary.hra))
        self.ta = QLineEdit()
        self.ta.setReadOnly(True)
        self.ta.setText(str(self.salary.ta))
        self.it = QLineEdit()
        self.it.setReadOnly(True)
        self.it.setText(str(self.salary.it))
        self.pt = QLineEdit()
        self.pt.setReadOnly(True)
        self.pt.setText(str(self.salary.pt))

        self.grossAllowance = QLineEdit()
        self.grossAllowance.setReadOnly(True)
        self.grossAllowance.setText(str(self.salary.grossEarnings))
        self.grossDeduction = QLineEdit()
        self.grossDeduction.setReadOnly(True)
        self.grossDeduction.setText(str(self.salary.grossDeductions))

        self.netPay = QLineEdit()
        self.netPay.setReadOnly(True)
        self.netPay.setText(str(self.salary.netPay))

        self.setupUI()


    def setupUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)
        layout.addWidget(QLabel("Salary for the month of %s, %s\n"%(self.month, self.year)))

        form1 = QFormLayout()
        form1.addRow(QLabel("ID No."), self.id)
        form1.addRow(QLabel("Name"), self.name)
        form1.addRow(QLabel("Designation"), self.designation)
        form1.addRow(QLabel("Original Pay"), self.originalPay)
        form1.addRow(QLabel("Original Pay Grade"), self.originalPayGrade)
        form1.addRow(QLabel("Date of joining"), self.DOJ)
        form1.addRow(QLabel("Pan No."), self.pan)

        infoGroup = QGroupBox("Basic Info")
        infoGroup.setLayout(form1)
        layout.addWidget(infoGroup)

        earningForm = QFormLayout()
        earningForm.addRow(QLabel("Present Pay"), self.presentPay)
        earningForm.addRow(QLabel("Dearness Allowance"), self.da)
        earningForm.addRow(QLabel("House Rent Allowance"), self.hra)
        earningForm.addRow(QLabel("Transport Allowance"), self.ta)
        earningForm.addRow(QLabel("Gross Earnings"), self.grossAllowance)

        leftGroup = QGroupBox("Allowances")
        leftGroup.setLayout(earningForm)


        deductionsForm = QFormLayout()
        deductionsForm.addRow(QLabel("Income Tax"), self.it)
        deductionsForm.addRow(QLabel("Profession Tax"), self.pt)
        deductionsForm.addRow(QLabel("Gross Deductions"), self.grossDeduction)

        rightGroup = QGroupBox("Deductions")
        rightGroup.setLayout(deductionsForm)

        table = QHBoxLayout()
        table.addWidget(leftGroup)
        table.addWidget(rightGroup)
        layout.addLayout(table)

        netPayLayout = QHBoxLayout()
        netPayLayout.addWidget(QLabel("Net Pay"))
        netPayLayout.addWidget(self.netPay)
        netPayLayout.addStretch()
        layout.addLayout(netPayLayout)

        self.bttnPrint = QPushButton("Confirm")
        self.bttnPrint.clicked.connect(self.printSlip)
        self.bttnCancel = QPushButton("Back")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnPrint.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")

        layout.addStretch()
        bttnLayout = QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnCancel)
        bttnLayout.addWidget(self.bttnPrint)

        layout.addLayout(bttnLayout)
        self.setLayout(layout)

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def printSlip(self):
        try:
            Database.getdb().saveSalary(self.salary)
            printPaySlip(*self.salary.result())
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                choice = QtGui.QMessageBox.question(self, 'Replace?',
                                                    "Salary calculation of " + self.salary.id + " for " + self.salary.month
                                                    + ", " + str(self.salary.year) + " already exists! Do you want to replace it?",
                                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if choice == QtGui.QMessageBox.Yes:
                    try:
                        Database.getdb().replaceSalary(self.salary)
                        printPaySlip(*self.salary.result())
                    except mysql.connector.Error as e:
                        ShowMysqlError(e)
            else:
                ShowMysqlError(e)
