from PySide import QtGui, QtCore
from PySide.QtGui import QWidget, QLineEdit, QRegExpValidator, QComboBox, QPushButton, QLabel,\
    QHBoxLayout, QFormLayout, QVBoxLayout, QMessageBox, QDoubleValidator, QGroupBox, QFrame
from PySide.QtCore import QRegExp, QDate

from CustomClasses import Employee
from CustomWidgets import DatePicker, SearchBox, ValidatingLineEdit
from DatabaseManager import Database

import mysql.connector
from ShowMySqlError import ShowMysqlError

class EditEmployeeWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Edit Employee"

        # ------elements for selecting employee-----------
        self.nameSearch = SearchBox(self)
        self.nameSearch.setPlaceholderText("Enter Name")

        # self.name.currentIndexChanged.connect(self.setIDList)
        self.nameList = []
        self.nameList = Database.getdb().getEmployeeNameList()
        self.nameSearch.setList(self.nameList)
        self.nameSearch.setCurrentIndex(-1)

        self.id = QComboBox()
        self.id.currentIndexChanged.connect(lambda: self.loadInfo(self.id.currentText()))
        self.nameSearch.returnPressed.connect(self.setIDList)

        # ------elements for ediiting employee-----------
        self.nameEdit = ValidatingLineEdit("Name", "[a-zA-Z\s]+", self)
        self.designation = QComboBox(self)
        self.originalPay = ValidatingLineEdit("Original Pay", QDoubleValidator(), self)
        self.originalPayGrade = ValidatingLineEdit("Original Pay Grade", QDoubleValidator(), self)
        self.DOJ = DatePicker(self)
        self.pan = ValidatingLineEdit("PAN", "[A-Z]{5}\d{4}[A-Z]", self)
        self.inputs = [self.nameEdit, self.originalPay, self.originalPayGrade, self.pan]

        self.bttnSave = QPushButton("Save Changes")
        self.bttnCancel = QPushButton("Back")
        self.bttnSave.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnSave.clicked.connect(self.save)

        self.designation.addItems(Database.getdb().getDesignations())
        self.nameSearch.editTextChanged.connect(self.clearInfo)
        self.clearInfo()

        self.setupUI()

    def save(self):
        valid = True
        if len(self.id.currentText()) == 0:
            QMessageBox(QMessageBox.Information, "Error", "Please select name and ID!", parent=self).exec_()
            valid = False
        else:
            for i in range(len(self.inputs)):
                if not self.inputs[i].isValid():
                    valid = False
                    QtGui.QMessageBox(QtGui.QMessageBox.Information, "Error", self.inputs[i].getErrorMessage(),
                                            parent=self).exec_()
                    break

        if valid:
            emp = Employee(self.id.currentText(),
                           self.nameEdit.text(),
                           self.designation.currentText(),
                           self.originalPay.text(),
                           self.originalPayGrade.text(),
                           self.DOJ.getDate(),
                           self.pan.text())
            try:
                Database.getdb().editEmployee(emp)
            except mysql.connector.Error as e:
                ShowMysqlError(e, self)
                return

            QMessageBox(QMessageBox.NoIcon, "Success", "Employee edited successfully", parent=self).exec_()

    def setInputReadOnly(self, TrueOrFalse):
        self.nameEdit.setReadOnly(TrueOrFalse)
        self.originalPay.setReadOnly(TrueOrFalse)
        self.originalPayGrade.setReadOnly(TrueOrFalse)
        self.DOJ.setReadOnly(TrueOrFalse)
        self.pan.setReadOnly(TrueOrFalse)
        # reload stylesheet to refelect changes of readonly
        self.nameEdit.setStyle(self.style())
        self.originalPay.setStyle(self.style())
        self.originalPayGrade.setStyle(self.style())
        self.DOJ.setStyle(self.style())
        self.pan.setStyle(self.style())

    def clearInfo(self):
        self.id.setCurrentIndex(-1)
        self.nameEdit.clear()
        self.designation.setCurrentIndex(-1)
        self.originalPay.clear()
        self.originalPayGrade.clear()
        self.DOJ.clear()
        self.pan.clear()

        self.setInputReadOnly(True)
        # self.nameEdit.setReadOnly(True)
        # self.originalPay.setReadOnly(True)
        # self.originalPayGrade.setReadOnly(True)
        # self.DOJ.setReadOnly(True)
        # self.pan.setReadOnly(True)
        # # reload stylesheet to refelect changes of readonly
        # self.nameEdit.setStyle(self.style())
        # self.originalPay.setStyle(self.style())
        # self.originalPayGrade.setStyle(self.style())
        # self.DOJ.setStyle(self.style())
        # self.pan.setStyle(self.style())

    def setIDList(self, name):
        self.id.clear()
        self.id.addItems(Database.getdb().getIdListForName(name))

    def loadInfo(self, id):
        print "id =", id, "...", len(id)
        if id != '':
            emp = Database.getdb().getEmployeeInfo(id)
            self.nameEdit.setText(emp.name)
            self.designation.setCurrentIndex(self.designation.findText(emp.designation))
            self.originalPay.setText(str(emp.originalPay))
            self.originalPayGrade.setText(str(emp.originalPayGrade))
            self.DOJ.setDate(emp.getQDate())
            self.pan.setText(emp.pan)

            self.setInputReadOnly(False)
            # self.nameEdit.setReadOnly(False)
            # self.originalPay.setReadOnly(False)
            # self.originalPayGrade.setReadOnly(False)
            # self.DOJ.setReadOnly(False)
            # self.pan.setReadOnly(False)
            # # reload stylesheet to refelect changes of readonly
            # self.nameEdit.setStyle(self.style())
            # self.originalPay.setStyle(self.style())
            # self.originalPayGrade.setStyle(self.style())
            # self.DOJ.setStyle(self.style())
            # self.pan.setStyle(self.style())

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def setupUI(self):

        paneLayout = QHBoxLayout()
        paneLayout.setContentsMargins(0, 0, 0, 0)

        leftPane = QFrame()
        leftPane.setObjectName("leftPane")

        leftPaneLayout = QVBoxLayout()
        leftPaneLayout.setContentsMargins(20, 20, 20, 10)
        heading = QLabel("Select Employee: ")
        heading.setObjectName("heading")
        leftPaneLayout.addWidget(heading)
        leftPaneLayout.addSpacing(10)


        form1 = QFormLayout()
        form1.addRow(QLabel("Name"), self.nameSearch)
        form1.addRow(QLabel("ID No."), self.id)
        leftPaneLayout.addLayout(form1)
        leftPaneLayout.addStretch()
        leftPane.setLayout(leftPaneLayout  )

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)

        editGroup = QGroupBox("Edit below")
        form = QFormLayout()
        form.setContentsMargins(10, 10, 10, 30)
        form.setSpacing(20)
        form.addRow(QLabel("Name"), self.nameEdit)
        form.addRow(QLabel("Designation"), self.designation)
        form.addRow(QLabel("Original Pay"), self.originalPay)
        form.addRow(QLabel("Original Pay Grade"), self.originalPayGrade)
        form.addRow(QLabel("Date of joining"), self.DOJ)
        form.addRow(QLabel("Pan No."), self.pan)
        editGroup.setLayout(form)

        layout.addWidget(editGroup)
        layout.addStretch()
        bttnLayout = QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnCancel)
        bttnLayout.addWidget(self.bttnSave)

        layout.addLayout(bttnLayout)

        paneLayout.addWidget(leftPane)
        paneLayout.addLayout(layout)
        self.setLayout(paneLayout)