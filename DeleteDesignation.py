from PySide import QtGui
from DatabaseManager import Database


class DelDesignationWidget(QtGui.QWidget):
    """PySide widget that contains GUI for deleting an existing designation from the database

    This contains a dropdown box (``QComboBox``) for selecting name of designation that needs to be deleted.
    After selecting the required designation name from there, the designation info is automatically loaded into
    some input boxes on screen.  These input boxes are created using ``QLineEdit`` module.

    A 'Delete' button (``QPushButton``) is present at the bottom. Clicking 'Delete' checks if there are any employees
    with this designation in the database. In that case the designation can not be deleted. Otherwise user is asked for
    confirmation and then the designation in s deleted.
    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Edit Designation"

        self.chooseDesignation = QtGui.QComboBox()
        self.loadDesignations()

        self.designation = QtGui.QLineEdit()
        self.da = QtGui.QLineEdit()
        self.hra = QtGui.QLineEdit()
        self.ta = QtGui.QLineEdit()
        self.it = QtGui.QLineEdit()
        self.pt = QtGui.QLineEdit()
        self.inputs = [self.designation, self.da, self.hra, self.ta, self.it, self.pt]
        self.setInputReadOnly(True)

        self.chooseDesignation.currentIndexChanged.connect(lambda: self.loadInfo(self.chooseDesignation.currentText()))
        self.clearInfo()

        self.bttnCancel = QtGui.QPushButton("Back")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnDel = QtGui.QPushButton("Delete")
        self.bttnDel.clicked.connect(self.removeDesignation)
        self.bttnDel.setObjectName("CancelButton")
        self.bttnCancel.setObjectName("OkButton")

        self.setUpUI()

    def setInputReadOnly(self, TrueOrFalse):
        for i in range(len(self.inputs)):
            self.inputs[i].setReadOnly(TrueOrFalse)
            self.inputs[i].setStyle(self.style())

    def clearInfo(self):
        for i in range(len(self.inputs)):
            self.inputs[i].clear()

    def loadInfo(self, designation):
        if designation != "":
            self.designation.setText(designation)
            desig = Database.getdb().getDesignationInfo(designation)
            self.da.setText(str(desig.da))
            self.hra.setText(str(desig.hra))
            self.ta.setText(str(desig.ta))
            self.it.setText(str(desig.it))
            self.pt.setText(str(desig.pt))

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def loadDesignations(self):
        self.chooseDesignation.clear()
        self.desigList = Database.getdb().getDesignations()
        self.chooseDesignation.addItems(self.desigList)
        self.chooseDesignation.setCurrentIndex(-1)

    def removeDesignation(self):
        origDesig = self.chooseDesignation.currentText()
        if len(origDesig) == 0:
            QtGui.QMessageBox(QtGui.QMessageBox.Information, "Error", "Please select a Designation to edit!", parent=self).exec_()

        elif Database.getdb().employeeWithDesigExists(origDesig):
            QtGui.QMessageBox(QtGui.QMessageBox.Information, "Error", "Unable to delete! Employees with this designation exist!",
                              parent=self).exec_()
        else:
            choice = QtGui.QMessageBox.question(self, 'Confirmation',
                                                "Are you sure you want to delete this designation?",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:
                try:
                    Database.getdb().delDesignation(origDesig)
                    msg = QtGui.QMessageBox(QtGui.QMessageBox.NoIcon, "Success", "Deleted Successfully", parent=self)
                    msg.exec_()
                    # reload name list
                    self.chooseDesignation.clear()
                    self.loadDesignations()
                    self.clearInfo()

                except Exception as e:
                    raise e

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

        editGroup = QtGui.QGroupBox("Details shown below")
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
        bttnLayout.addWidget(self.bttnDel)

        layout.addLayout(bttnLayout)

        paneLayout.addWidget(leftPane)
        paneLayout.addLayout(layout)
        self.setLayout(paneLayout)

