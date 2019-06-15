from PySide import QtGui, QtCore

'''
Home Page
----------
This will have Buttons to open all other pages of this application. 
'''

class HomeWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Home"
        self.logo = QtGui.QLabel()
        self.logo.setPixmap("Resources/iiitk.png")
        self.bttnAddEmployee = NavButton("Add Employee", "Resources/add_user.png", "Add Employee", self)
        self.bttnEditEmp = NavButton("Edit Employee", "Resources/edit_user.png", "Edit Employee", self)
        self.bttnDelEmp = NavButton("Delete Employee", "Resources/delete_user.png", "Del Employee", self)
        self.bttnShowEmp = NavButton("Show Employee", "Resources/show_user.png", "Show Employee", self)
        self.bttnAddDesignation = NavButton("Add Designation", "Resources/add_designation.png", "Add Designation", self)
        self.bttnEditDesg = NavButton("Edit Designation", "Resources/edit_designation.png", "Edit Designation", self)
        self.bttnDelDesg = NavButton("Delete Designation", "Resources/delete_designation.png", None, self)
        self.bttnShowDesg = NavButton("Show Designations", "Resources/show_designation.png", "Show Designation", self)
        self.bttnCalcSalary = NavButton("Generate Payslip", "Resources/rupee.png", "Calc Salary", self)
        self.bttnSettings = NavButton("Settings", "Resources/icons8-settings-96.png", None, self)
        self.setupUI()

    def gotoPage(self, name):
        if self.__parent is not None:
            self.__parent.gotoPage(name)

    def setupUI(self):
        layout = QtGui.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignHCenter)

        self.setContentsMargins(20, 10, 20, 5)

        bttnList = [self.bttnAddDesignation, self.bttnDelDesg, self.bttnEditDesg, self.bttnShowDesg,
                    self.bttnShowEmp, self.bttnEditEmp, self.bttnAddEmployee, self.bttnDelEmp,
                    self.bttnSettings, self.bttnCalcSalary]
        for bttn in bttnList:
            bttn.setObjectName("HomeBttn")
            bttn.setIconSize(QtCore.QSize(55,55))

        employeeGroup = QtGui.QGroupBox("Employee")
        employeeGroupLayout = QtGui.QVBoxLayout()
        employeeGroupLayout.addWidget(self.bttnAddEmployee)
        employeeGroupLayout.addWidget(self.bttnEditEmp)
        employeeGroupLayout.addWidget(self.bttnDelEmp)
        employeeGroupLayout.addWidget(self.bttnShowEmp)
        employeeGroup.setLayout(employeeGroupLayout)

        designationGroup = QtGui.QGroupBox("Designation")
        designationGroupLayout = QtGui.QVBoxLayout()
        designationGroupLayout.addWidget(self.bttnAddDesignation)
        designationGroupLayout.addWidget(self.bttnEditDesg)
        designationGroupLayout.addWidget(self.bttnDelDesg)
        designationGroupLayout.addWidget(self.bttnShowDesg)
        designationGroup.setLayout(designationGroupLayout)

        groups = QtGui.QHBoxLayout()
        groups.addWidget(employeeGroup)
        groups.addWidget(designationGroup)

        otherBttns = QtGui.QGroupBox()
        otherBttnsLayout = QtGui.QVBoxLayout()
        otherBttnsLayout.addWidget(self.bttnCalcSalary)
        otherBttnsLayout.addWidget(self.bttnSettings)
        otherBttnsLayout.addStretch()
        otherBttns.setLayout(otherBttnsLayout)
        groups.addWidget(otherBttns)

        groups.addStretch()

        layout.addLayout(groups)

        layout.addStretch()

        centerLayout = QtGui.QHBoxLayout()
        centerLayout.addStretch()
        centerLayout.addLayout(layout)
        centerLayout.addStretch()
        self.setLayout(centerLayout)

class NavButton(QtGui.QPushButton):
    def __init__(self, text, img, page, parent):
        QtGui.QPushButton.__init__(self, text, parent=parent)
        self.setIcon(QtGui.QIcon(QtGui.QPixmap(img)))
        if page is not None:
            self.clicked.connect(lambda: parent.gotoPage(page))
