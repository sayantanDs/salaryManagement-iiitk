from PySide import QtGui, QtCore
from DatabaseManager import Database
import mysql.connector
from ShowMySqlError import ShowMysqlError


class EditDesignationWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Edit Designation"

        self.chooseDesig = QtGui.QComboBox()
        self.loadDesignations()


        self.desig = QtGui.QLineEdit()
        self.da = QtGui.QLineEdit()
        self.ha = QtGui.QLineEdit()
        self.ta = QtGui.QLineEdit()
        self.it = QtGui.QLineEdit()
        self.pt = QtGui.QLineEdit()
        self.chooseDesig.currentIndexChanged.connect(lambda: self.loadInfo(self.chooseDesig.currentText()))

        self.clearInfo()


        self.bttnCancel = QtGui.QPushButton("Back")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnSave = QtGui.QPushButton("Save")
        self.bttnSave.clicked.connect(self.changeDetails)
        self.bttnSave.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")


        self.setUpUI()

    def clearInfo(self):
        self.desig.clear()
        self.da.clear()
        self.ha.clear()
        self.ta.clear()
        self.it.clear()
        self.pt.clear()

        self.desig.setReadOnly(True)
        self.da.setReadOnly(True)
        self.ha.setReadOnly(True)
        self.ta.setReadOnly(True)
        self.it.setReadOnly(True)
        self.pt.setReadOnly(True)

        self.desig.setStyle(self.style())
        self.da.setStyle(self.style())
        self.ha.setStyle(self.style())
        self.ta.setStyle(self.style())
        self.it.setStyle(self.style())
        self.pt.setStyle(self.style())



    def loadInfo(self, designation):
        if designation != "":
            self.desig.setText(designation)
            designation, d_a, h_a, t_a, i_t, p_t = Database.getdb().getDesignationInfo(designation)
            self.da.setText(str(d_a))
            self.ha.setText(str(h_a))
            self.ta.setText(str(t_a))
            self.it.setText(str(i_t))
            self.pt.setText(str(p_t))

            self.desig.setReadOnly(False)
            self.da.setReadOnly(False)
            self.ha.setReadOnly(False)
            self.ta.setReadOnly(False)
            self.it.setReadOnly(False)
            self.pt.setReadOnly(False)

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def loadDesignations(self):
        self.chooseDesig.clear()
        self.desigList = Database.getdb().getDesignations()
        self.chooseDesig.addItems(self.desigList)
        self.chooseDesig.setCurrentIndex(-1)

    def changeDetails(self):
        field = self.chooseDesig.currentText()
        desg = self.desig.text()
        da = self.da.text()
        ha = self.ha.text()
        ta = self.ta.text()
        it = self.it.text()
        pt = self.pt.text()

        print desg, da + ha + ta + it + pt
        if "" in [desg, da, ha, ta, it, pt]:
            msg = QtGui.QMessageBox(QtGui.QMessageBox.Information, "Error", "Please enter all the information!", parent=self)
            msg.exec_()
        else:
            try:
                Database.getdb().editDesignationInfo(desg, da, ha, ta, it, pt, field)
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
        leftPaneLayout.addWidget(self.chooseDesig)
        leftPaneLayout.addStretch()
        leftPane.setLayout(leftPaneLayout)

        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)

        editGroup = QtGui.QGroupBox("Edit below")
        form = QtGui.QFormLayout()
        form.setContentsMargins(10, 10, 10, 30)
        form.setSpacing(20)
        form.addRow(QtGui.QLabel("Designation:"), self.desig)
        form.addRow(QtGui.QLabel("DA:"), self.da)
        form.addRow(QtGui.QLabel("HA:"), self.ha)
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

