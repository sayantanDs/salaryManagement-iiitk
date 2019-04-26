from PySide.QtGui import QWidget, QPushButton, QLabel,\
        QLineEdit, QHBoxLayout, QFormLayout, QVBoxLayout, QMessageBox, QDoubleValidator

import DatabaseManager

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

        self.designation = QLineEdit()
        self.da = QLineEdit()
        self.da.setValidator(QDoubleValidator())
        self.hra = QLineEdit()
        self.hra.setValidator(QDoubleValidator())
        self.ta = QLineEdit()
        self.ta.setValidator(QDoubleValidator())
        self.it = QLineEdit()
        self.it.setValidator(QDoubleValidator())
        self.pt = QLineEdit()
        self.pt.setValidator(QDoubleValidator())

        self.bttnAddDesignation = QPushButton("Add Designation")
        self.bttnCancel = QPushButton("Cancel")
        self.bttnAddDesignation.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnAddDesignation.clicked.connect(self.add)

        self.setupUI()

    def add(self):
        designation = self.designation.text()
        da = self.da.text()
        hra = self.hra.text()
        ta = self.ta.text()
        it = self.it.text()
        pt = self.pt.text()

        if "" in [designation, da, hra, ta, it, pt]:
            msg = QMessageBox(QMessageBox.Information, "Error", "Please enter all the information!", parent=self)
            msg.exec_()
        else:
            print designation, float(da), float(hra), float(ta), float(it), float(pt)
            try:
                DatabaseManager.db.addDesignation(designation, float(da), float(hra), float(ta), float(it), float(pt))
                msg = QMessageBox(QMessageBox.NoIcon, "Success", "Designation added successfully", parent=self)
                msg.exec_()
                self.goBack()

            except Exception as e:
                msg = QMessageBox(QMessageBox.Critical, "Error", str(e), parent=self)
                msg.exec_()

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