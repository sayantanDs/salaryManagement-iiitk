from PySide import QtGui
from DatabaseManager import Database
import mysql.connector
from ShowMySqlError import ShowMysqlError
from CustomWidgets import ValidatingLineEdit
from CustomClasses import Designation


class EditDesignationWidget(QtGui.QWidget):
    """PySide widget that contains GUI for editing an existing designation from the database

    This contains a dropdown box (``QComboBox``) for selecting name of designation that needs to be edited.
    After selecting the required designation name from there, the designation info is automatically loaded into
    some input boxes on screen.  These input boxes are created using ``ValidatingLineEdit`` module.
    User may make necessary changes in these boxes. These boxes will also give a feedback that is the edited
    input valid or not (as they are created using ``ValidatingLineEdit``)

    A 'Save' button (``QPushButton``) is present at the bottom. Clicking 'Save' checks if all inputs are valid.
    If any of the inputs are invalid, error message is shown for the first invalid input.
    If all inputs are valid, a ``Designation`` object is created from edited info and passed to
    ``editDesignationInfo()`` method of DatabaseManager module to update the designation record
    in Database.

    See Also:
        - :py:mod:`ValidatingLineEdit <CustomWidgets.validatingLineEdit.ValidatingLineEdit>` widget from CustomWidgets
        - :py:mod:`Designation <CustomClasses.Designation.Designation>` class from CustomClasses
        - :py:meth:`editDesignationInfo() <DatabaseManager.databaseManager.DatabaseManager.editDesignationInfo>` method of DatabaseManager
    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Edit Designation"

        self.chooseDesignation = QtGui.QComboBox()
        self.loadDesignations()

        self.designation = ValidatingLineEdit("Designation", "[a-zA-Z0-9-_\s]+", self)
        self.da = ValidatingLineEdit("Dearness Allowance", QtGui.QDoubleValidator(), self)
        self.hra = ValidatingLineEdit("House Rent Allowance", QtGui.QDoubleValidator(), self)
        self.ta = ValidatingLineEdit("Transport Allowance", QtGui.QDoubleValidator(), self)
        self.it = ValidatingLineEdit("Income Tax", QtGui.QDoubleValidator(), self)
        self.pt = ValidatingLineEdit("Professional Tax", QtGui.QDoubleValidator(), self)
        self.inputs = [self.designation, self.da, self.hra, self.ta, self.it, self.pt]

        self.chooseDesignation.currentIndexChanged.connect(lambda: self.loadInfo(self.chooseDesignation.currentText()))
        self.clearInfo()

        self.bttnCancel = QtGui.QPushButton("Back")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnSave = QtGui.QPushButton("Save")
        self.bttnSave.clicked.connect(self.changeDetails)
        self.bttnSave.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")

        self.setUpUI()

    def setInputReadOnly(self, TrueOrFalse):
        for i in range(len(self.inputs)):
            self.inputs[i].setReadOnly(TrueOrFalse)
            self.inputs[i].setStyle(self.style())

    def clearInfo(self):
        for i in range(len(self.inputs)):
            self.inputs[i].clear()
        self.setInputReadOnly(True)

    def loadInfo(self, designation):
        if designation != "":
            self.designation.setText(designation)
            desig = Database.getdb().getDesignationInfo(designation)
            self.da.setText(str(desig.da))
            self.hra.setText(str(desig.hra))
            self.ta.setText(str(desig.ta))
            self.it.setText(str(desig.it))
            self.pt.setText(str(desig.pt))
            self.setInputReadOnly(False)

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def loadDesignations(self):
        self.chooseDesignation.clear()
        self.desigList = Database.getdb().getDesignations()
        self.chooseDesignation.addItems(self.desigList)
        self.chooseDesignation.setCurrentIndex(-1)

    def changeDetails(self):
        origDesig = self.chooseDesignation.currentText()
        valid = True
        if len(origDesig) == 0:
            QtGui.QMessageBox(QtGui.QMessageBox.Information, "Error", "Please select a Designation to edit!", parent=self).exec_()
            valid = False
        else:
            for i in range(len(self.inputs)):
                if not self.inputs[i].isValid():
                    QtGui.QMessageBox(QtGui.QMessageBox.Information, "Error", self.inputs[i].getErrorMessage(), parent=self).exec_()
                    valid = False
                    break
        if valid:
            desig = Designation(self.designation.text(),
                               self.da.text(),
                               self.hra.text(),
                               self.ta.text(),
                               self.it.text(),
                               self.pt.text())
            try:
                Database.getdb().editDesignationInfo(desig, origDesig)
                self.loadDesignations()
                self.clearInfo()
            except mysql.connector.Error as e:
                ShowMysqlError(e, self)
                return
            QtGui.QMessageBox(QtGui.QMessageBox.NoIcon, "Success", "Designation edited successfully", parent=self).exec_()

    def setUpUI(self):

        paneLayout = QtGui.QHBoxLayout()
        paneLayout.setContentsMargins(0, 0, 0, 0)

        leftPane = QtGui.QFrame()
        leftPane.setObjectName("leftPane")

        leftPaneLayout = QtGui.QVBoxLayout()
        leftPaneLayout.setContentsMargins(20, 20, 20, 10)
        heading = QtGui.QLabel("Select Designation: ")
        heading.setObjectName("heading")
        leftPaneLayout.addWidget(heading)
        leftPaneLayout.addSpacing(10)
        leftPaneLayout.addWidget(self.chooseDesignation)
        leftPaneLayout.addStretch()
        leftPane.setLayout(leftPaneLayout)

        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)

        editGroup = QtGui.QGroupBox("Edit below")
        form = QtGui.QFormLayout()
        form.setContentsMargins(10, 10, 10, 30)
        form.setSpacing(20)
        form.addRow(QtGui.QLabel("Designation:"), self.designation)
        form.addRow(QtGui.QLabel("DA:"), self.da)
        form.addRow(QtGui.QLabel("HA:"), self.hra)
        form.addRow(QtGui.QLabel("TA:"), self.ta)
        form.addRow(QtGui.QLabel("IT:"), self.it)
        form.addRow(QtGui.QLabel("PT:"), self.pt)
        editGroup.setLayout(form)

        layout.addWidget(editGroup)
        layout.addStretch()
        bttnLayout = QtGui.QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnCancel)
        bttnLayout.addWidget(self.bttnSave)

        layout.addLayout(bttnLayout)

        paneLayout.addWidget(leftPane)
        paneLayout.addLayout(layout)
        self.setLayout(paneLayout)

