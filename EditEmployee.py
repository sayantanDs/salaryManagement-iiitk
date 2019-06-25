from PySide import QtGui, QtCore
from PySide.QtGui import QWidget, QLineEdit, QRegExpValidator, QComboBox, QPushButton, QLabel,\
    QHBoxLayout, QFormLayout, QVBoxLayout, QMessageBox, QDoubleValidator, QGroupBox, QFrame

from CustomClasses import Employee
from CustomWidgets import DatePicker, SearchBox, ValidatingLineEdit
from DatabaseManager import Database

import mysql.connector
from ShowMySqlError import ShowMysqlError


class EditEmployeeWidget(QWidget):
    """PySide widget that contains GUI for editing existing employee record from the database

    This contains a ``SearchBox`` for selecting name of employee who's record needs to be edited. Selecting the name
    automatically loads IDs of all employees with that name (in case multiple employees have exact same name) in
    a dropdown box (``QComboBox``). After selecting the required ID from there, the employee info
    is automatically loaded into some input boxes on screen.
    These input boxes are created using ``ValidatingLineEdit`` module.
    User may make necessary changes in these boxes. These boxes will also give a feedback that is the edited
    input valid or not (as they are created using ``ValidatingLineEdit``)

    A 'Save' button (``QPushButton``) is present at the bottom. Clicking it checks if all inputs are valid.
    If any of the inputs are invalid, error message is shown for the first invalid input.
    Otherwise, an ``Employee`` object is created from the edited info and passed to
    ``editEmployee()`` method of DatabaseManager module to update the employee record
    in Database.


    See Also:
        - :py:mod:`SearchBox <CustomWidgets.searchBox.SearchBox>` widget from CustomWidgets
        - :py:mod:`ValidatingLineEdit <CustomWidgets.validatingLineEdit.ValidatingLineEdit>` class from CustomWidgets
        - :py:mod:`Employee <CustomClasses.Employee.Employee>` class from CustomClasses
        - :py:meth:`editEmployee() <DatabaseManager.databaseManager.DatabaseManager.editEmployee>` method of DatabaseManager

    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Edit Employee"

        # ------elements for selecting employee-----------
        self.nameSearch = SearchBox(self)
        self.nameSearch.setPlaceholderText("Enter Name")

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