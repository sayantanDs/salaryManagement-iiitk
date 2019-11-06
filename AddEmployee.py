from PySide import QtGui
from CustomWidgets import DatePicker
from DatabaseManager import Database
import mysql.connector
from ShowMySqlError import ShowMysqlError
from CustomWidgets import ValidatingLineEdit
from CustomClasses import Employee


class AddEmployeeWidget(QtGui.QWidget):
    """PySide widget that contains GUI for adding a new employee to the database

        It has input boxes in a form layout where one can enter info about employee. These input boxes are created
        using ValidatingLineEdit.
        A 'Add Employee' button (``QPushButton``) is present at the bottom. Clicking it checks if all inputs are valid.
        If all inputs are valid, it proceeds to add the new employee record to Database by passing the info
        to addEmployee function of DatabaseManager.
        If any of the inputs are invalid, error message is shown for the first invalid input.

        See Also:
            - :py:mod:`ValidatingLineEdit <CustomWidgets.validatingLineEdit.ValidatingLineEdit>` class from CustomWidgets
            - :py:mod:`Employee <CustomClasses.Employee.Employee>` class from CustomClasses
            - :py:meth:`addEmployee() <DatabaseManager.databaseManager.DatabaseManager.addEmployee>` method of DatabaseManager

    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Add Employee"

        self.id = ValidatingLineEdit("ID", "[a-zA-Z0-9-_]+", self)
        self.name = ValidatingLineEdit("Name", "[a-zA-Z\s]+", self)
        self.designation = QtGui.QComboBox(self)
        self.designation.addItems(Database.getdb().getDesignations())
        self.originalPay = ValidatingLineEdit("Original Pay", QtGui.QDoubleValidator(), self)
        self.gradePay = ValidatingLineEdit("Grade Pay", QtGui.QDoubleValidator(), self)
        self.DOJ = DatePicker(self)
        self.pan = ValidatingLineEdit("PAN", "[A-Z]{5}\d{4}[A-Z]", self)
        self.pan.textEdited.connect(lambda s: self.pan.setText(str(s).upper()))

        # inputs whos validity needs to checked are put in a list
        # so that we can loop through them to check validity
        self.inputs = [self.id, self.name, self.originalPay, self.gradePay, self.pan]

        self.bttnAddEmployee = QtGui.QPushButton("Add Employee")
        self.bttnCancel = QtGui.QPushButton("Cancel")
        self.bttnAddEmployee.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnAddEmployee.clicked.connect(self.add)

        self.setupUI()

    def add(self):
        """This method is automatically called on clicking 'Add Employee' button

        This first checks if all inputs are valid. If any of the inputs are invalid, error message
        is shown for the first invalid input, else a new Employee object is created from available info.
        This Employee object is then passed to addEmployee() function of DatabaseManager which adds
        a new employee record in the database.
        """

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
                           self.gradePay.text(),
                           self.DOJ.getDate(),
                           self.pan.text())
            try:
                Database.getdb().addEmployee(emp)
                QtGui.QMessageBox(QtGui.QMessageBox.NoIcon, "Success", "Employee added successfully",
                                  parent=self).exec_()
                self.goBack()
            except mysql.connector.Error as e:
                ShowMysqlError(e, self)
                return

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()


    def setupUI(self):
        """Arranges GUI elements inside the widget properly"""

        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)
        form = QtGui.QFormLayout()
        form.setSpacing(20)
        form.addRow(QtGui.QLabel("ID No."), self.id)
        form.addRow(QtGui.QLabel("Name"), self.name)
        form.addRow(QtGui.QLabel("Designation"), self.designation)
        form.addRow(QtGui.QLabel("Original Pay"), self.originalPay)
        form.addRow(QtGui.QLabel("Original Pay Grade"), self.gradePay)
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