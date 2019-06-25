from PySide.QtGui import QWidget, QApplication, QPushButton, QLabel,\
        QLineEdit, QComboBox, QHBoxLayout, QFormLayout, QVBoxLayout, QMessageBox, QFrame, QFileDialog, QSpinBox, QGroupBox
from datetime import datetime

from CustomClasses import Designation, Salary
from DatabaseManager import Database
from CustomWidgets import SearchBox, ValueBox
from ShowMySqlError import ShowMysqlError

class CalculateSalaryWidget(QWidget):
    """A PySide widget which provides GUI for selecting employee and calculating salary for a month & year

    Tis contains boxes for month and year input. Enter the month and year of salary to be calculated here. This is
    initially automatically set to present month and year.

    Also contains a ``SearchBox`` for selecting name of employee who's salary needs to be calculated. Selecting the name
    automatically loads IDs of all employees with that name (in case multiple employees have exact same name) in
    a dropdown box (``QComboBox``). After selecting the required ID from there, the employee info
    is automatically loaded.

    The allowances and deductions are loaded in ``ValueBoxes`` and hence may be edited if required.

    After selecting everything, user needs to click 'calculate' button. This creates a ``Salary`` object from
    available info. The actual salary calculation takes place inside ``Salary`` class. This salary object is then
    passed to ``ShowPaySlipWidget`` which shows the final result and has option to confirm the calculation and print
    the payslip.

    Note:
        To automatically call functions on GUI interaction such as button click, PySide Signal and Slots are used.
        visit http://zetcode.com/gui/pysidetutorial/eventsandsignals/ for more on PySide Signal and Slots.

    See Also:
        - :py:mod:`SearchBox <CustomWidgets.searchBox.SearchBox>` widget from CustomWidgets
        - :py:mod:`ValueBox <CustomWidgets.valueBox.ValueBox>` widget from CustomWidgets
        - :py:mod:`Salary <CustomClasses.Salary.Salary>` class from CustomClasses
        - :py:mod:`ShowPaySlipWidget <ShowPaySlip.ShowPaySlipWidget>`

    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Calculate Salary"

        self.__desig = None
        self.__emp = None

        t = datetime.now()
        self.month = QComboBox()
        self.month.addItems(["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
                             "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"])
        self.month.setCurrentIndex(t.month - 1)
        self.year = QSpinBox()
        self.year.setRange(1900, 3000)
        self.year.setValue(t.year)

        self.name = SearchBox(self)
        self.name.setPlaceholderText("Enter Name")

        self.nameList = []
        self.nameList = Database.getdb().getEmployeeNameList()
        self.name.setList(self.nameList)

        self.id = QComboBox()

        self.designation = QLineEdit()
        self.designation.setReadOnly(True)
        self.originalPay = QLineEdit()
        self.originalPay.setReadOnly(True)
        self.originalPayGrade = QLineEdit()
        self.originalPayGrade.setReadOnly(True)
        self.DOJ = QLineEdit()
        self.DOJ.setReadOnly(True)
        self.pan = QLineEdit()
        self.pan.setReadOnly(True)

        self.presentPay = QLineEdit()
        self.presentPay.setReadOnly(True)
        self.da_percent = ValueBox()
        self.hra_percent = ValueBox()
        self.ta_percent = ValueBox()
        self.it_percent = ValueBox()
        self.pt_percent = ValueBox()

        self.name.editTextChanged.connect(self.clearInfo)

        self.bttnCalculate = QPushButton("Calculate")
        self.bttnCalculate.clicked.connect(self.calculate)
        self.bttnCancel = QPushButton("Back")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnCalculate.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")

        self.name.returnPressed.connect(self.setIDList)
        self.id.currentIndexChanged.connect(lambda: self.loadInfo(self.id.currentText()))

        self.setupUI()


    def calculate(self):
        """Automatically called on clicking calculate button"""

        if self.__emp is None:
            QMessageBox(QMessageBox.Information, "Error", "Please select an employee!", parent=self).exec_()
        else:
            if self.__parent is not None:
                self.__desig = Designation(self.__desig.designation,
                                                  self.da_percent.text(),
                                                  self.hra_percent.text(),
                                                  self.ta_percent.text(),
                                                  self.it_percent.text(),
                                                  self.pt_percent.text())
                salary = Salary(self.__emp, self.__desig, self.month.currentText(), self.year.text())
                self.__parent.gotoPage("Result", salary)

    def clearInfo(self):
        """Clears the contents of all input/display boxes"""

        self.id.setCurrentIndex(-1)
        self.designation.clear()
        self.originalPay.clear()
        self.originalPayGrade.clear()
        self.DOJ.clear()
        self.pan.clear()
        self.da_percent.clear()
        self.hra_percent.clear()
        self.ta_percent.clear()
        self.it_percent.clear()
        self.pt_percent.clear()
        self.__desig = None
        self.__emp = None

    def loadInfo(self, id):
        """Loads info for given ID in the GUI boxes. This automatically called on selecting an ID from GUI

        Args:
            id (str): ID of employee who's info needs to be loaded
        """
        print "id =", id, "...", len(id)
        if id != '':
            self.__emp = Database.getdb().getEmployeeInfo(id)
            self.designation.setText(self.__emp.designation)
            self.originalPay.setText(str(self.__emp.originalPay))
            self.originalPayGrade.setText(str(self.__emp.originalPayGrade))
            self.DOJ.setText(self.__emp.getStrDate())
            self.pan.setText(self.__emp.pan)

            self.__desig = Database.getdb().getDesignationInfo(self.__emp.designation)

            self.da_percent.setText(str(self.__desig.da))
            self.hra_percent.setText(str(self.__desig.hra))
            self.ta_percent.setText(str(self.__desig.ta))
            self.it_percent.setText(str(self.__desig.it))
            self.pt_percent.setText(str(self.__desig.pt))

    def setIDList(self, name):
        """Loads IDs of all employees with given name into the ID dropdown box

        This function is automatically called after selecting a name from the GUI

        Args:
            name (str): Name of employee
        """

        self.id.clear()
        self.id.addItems(Database.getdb().getIdListForName(name))

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def setupUI(self):
        """Arranges GUI elements inside the widget properly"""

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

        datelayout = QHBoxLayout()
        datelayout.addWidget(QLabel("Salary for month of "))
        datelayout.addWidget(self.month)
        datelayout.addWidget(self.year)
        datelayout.addStretch()
        leftPaneLayout.addLayout(datelayout)

        leftForm = QFormLayout()
        leftForm.setSpacing(10)
        leftForm.addRow(QLabel("Name"), self.name)
        leftForm.addRow(QLabel("ID No."), self.id)
        leftPaneLayout.addLayout(leftForm)

        leftPaneLayout.addStretch()
        leftPane.setLayout(leftPaneLayout)
        paneLayout.addWidget(leftPane)


        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)
        form = QFormLayout()
        form.setSpacing(10)
        form.addRow(QLabel("Designation"), self.designation)
        form.addRow(QLabel("Original Pay"), self.originalPay)
        form.addRow(QLabel("Original Pay Grade"), self.originalPayGrade)
        form.addRow(QLabel("Date of joining"), self.DOJ)
        form.addRow(QLabel("Pan No."), self.pan)

        infoGroup = QGroupBox("Basic Info")
        infoGroup.setLayout(form)
        layout.addWidget(infoGroup)

        leftForm = QFormLayout()
        leftForm.addRow(QLabel("Dearness Allowance"), self.da_percent)
        leftForm.addRow(QLabel("Housing Rent Allowance"),self.hra_percent)
        leftForm.addRow(QLabel("Transport Allowance"), self.ta_percent)

        leftGroup = QGroupBox("Allowances")
        leftGroup.setLayout(leftForm)

        rightForm = QFormLayout()
        rightForm.addRow(QLabel("Income Tax"), self.it_percent)
        rightForm.addRow(QLabel("Profession Tax"), self.pt_percent)

        rightGroup = QGroupBox("Deductions")
        rightGroup.setLayout(rightForm)

        table = QHBoxLayout()
        table.addWidget(leftGroup)
        table.addWidget(rightGroup)

        layout.addLayout(table)

        layout.addStretch()
        bttnLayout = QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnCancel)
        bttnLayout.addWidget(self.bttnCalculate)

        layout.addLayout(bttnLayout)

        paneLayout.addLayout(layout)
        self.setLayout(paneLayout)
