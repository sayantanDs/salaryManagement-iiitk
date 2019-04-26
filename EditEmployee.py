from PySide.QtGui import QWidget, QLineEdit, QRegExpValidator, QComboBox, QPushButton, QLabel,\
    QHBoxLayout, QFormLayout, QVBoxLayout, QMessageBox, QDoubleValidator, QGroupBox, QFrame
from PySide.QtCore import QRegExp, QDate

from CustomWidgets import DatePicker, SearchBox
import DatabaseManager

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
        self.nameList = DatabaseManager.db.getEmployeeNameList()
        self.nameSearch.setList(self.nameList)
        self.nameSearch.setCurrentIndex(-1)

        self.id = QComboBox()
        self.id.currentIndexChanged.connect(lambda: self.loadInfo(self.id.currentText()))
        self.nameSearch.returnPressed.connect(self.setIDList)

        # ------elements for ediiting employee-----------
        self.nameEdit = QLineEdit(self)
        self.nameEdit.setValidator(QRegExpValidator(QRegExp("[a-zA-Z\s]+")))
        self.designation = QComboBox(self)

        self.originalPay = QLineEdit(self)
        self.originalPay.setValidator(QDoubleValidator())
        self.originalPayGrade = QLineEdit(self)
        self.originalPayGrade.setValidator(QDoubleValidator())
        self.DOJ = DatePicker(self)
        self.pan = QLineEdit(self)
        self.pan.setValidator(QRegExpValidator(QRegExp("[A-Z]{5}\d{4}[A-Z]")))

        self.bttnSave = QPushButton("Save Changes")
        self.bttnCancel = QPushButton("Back")
        self.bttnSave.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnSave.clicked.connect(self.save)

        self.designation.addItems(DatabaseManager.db.getDesignations())
        self.nameSearch.editTextChanged.connect(self.clearInfo)
        self.clearInfo()

        self.setupUI()

    def save(self):
        id = self.id.currentText()
        name = self.nameEdit.text()
        designation = self.designation.currentText()
        originalPay = self.originalPay.text()
        originalPayGrade = self.originalPayGrade.text()
        doj = self.DOJ.getDate()
        doj = "%4d-%02d-%02d" % (doj.year(), doj.month(), doj.day())
        pan = self.pan.text()

        print name, designation, originalPay, originalPayGrade, doj, pan

        if "" in [id, name, designation, originalPay, originalPayGrade, doj, pan]:
            msg = QMessageBox(QMessageBox.Information, "Error", "Please enter all the information!", parent=self)
            msg.exec_()
        else:

            try:
                DatabaseManager.db.editEmployee(id, name, designation, float(originalPay), float(originalPayGrade), doj, pan)
            except mysql.connector.Error as e:
                ShowMysqlError(e, self)
                return

            QMessageBox(QMessageBox.NoIcon, "Success", "Employee edited successfully", parent=self).exec_()

    def clearInfo(self):
        self.id.setCurrentIndex(-1)
        self.nameEdit.clear()
        self.designation.setCurrentIndex(-1)
        self.originalPay.clear()
        self.originalPayGrade.clear()
        self.DOJ.clear()
        self.pan.clear()

        self.nameEdit.setReadOnly(True)
        self.originalPay.setReadOnly(True)
        self.originalPayGrade.setReadOnly(True)
        self.DOJ.setReadOnly(True)
        self.pan.setReadOnly(True)
        # reload stylesheet to refelect changes of readonly
        self.nameEdit.setStyle(self.style())
        self.originalPay.setStyle(self.style())
        self.originalPayGrade.setStyle(self.style())
        self.DOJ.setStyle(self.style())
        self.pan.setStyle(self.style())

    def setIDList(self, name):
        self.id.clear()
        self.id.addItems(DatabaseManager.db.getIdListForName(name))

    def loadInfo(self, id):
        print "id =", id, "...", len(id)
        if id != '':
            info = DatabaseManager.db.getEmployeeInfo(id)
            _, name, designation, originalPay, originalPayGrade, doj, pan = info
            # self.designation.setText(str(designation))
            self.nameEdit.setText(name)
            self.designation.setCurrentIndex(self.designation.findText(str(designation)))
            self.originalPay.setText(str(originalPay))
            self.originalPayGrade.setText(str(originalPayGrade))
            # self.DOJ.setText("%02d/%02d/%4d" % (doj.day, doj.month, doj.year))
            self.DOJ.setDate(QDate(doj.year, doj.month, doj.day))
            self.pan.setText(str(pan))

            self.nameEdit.setReadOnly(False)
            self.originalPay.setReadOnly(False)
            self.originalPayGrade.setReadOnly(False)
            self.DOJ.setReadOnly(False)
            self.pan.setReadOnly(False)
            # reload stylesheet to refelect changes of readonly
            self.nameEdit.setStyle(self.style())
            self.originalPay.setStyle(self.style())
            self.originalPayGrade.setStyle(self.style())
            self.DOJ.setStyle(self.style())
            self.pan.setStyle(self.style())

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