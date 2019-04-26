version_text = "v1_7_1 (online server) at freemysqlhosting.net"

from PySide.QtGui import QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QPixmap, QIcon, QGroupBox, QFont
from PySide.QtCore import Qt, QSize

from PySide.QtGui import QApplication
import sys


'''
Home Page
----------
This will have Buttons to open all other pages of this application. 
'''

class HomeWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__parent = parent
        self.title = "Home"

        self.logo = QLabel()
        self.logo.setPixmap("Resources/iiitk.png")

        self.bttnAddEmployee = QPushButton("Add Employee")
        self.bttnAddEmployee.setIcon(QIcon(QPixmap("Resources/add_user.png")))
        self.bttnAddEmployee.setIconSize(QSize(64,64))
        self.bttnAddEmployee.clicked.connect(lambda: self.gotoPage("Add Employee"))

        self.bttnEditEmp = QPushButton("Edit Employee")
        self.bttnEditEmp.setIcon(QIcon(QPixmap("Resources/edit_user.png")))
        self.bttnEditEmp.setIconSize(QSize(64, 64))
        self.bttnEditEmp.clicked.connect(lambda: self.gotoPage("Edit Employee"))

        self.bttnDelEmp = QPushButton("Delete Employee")
        self.bttnDelEmp.setIcon(QIcon(QPixmap("Resources/delete_user.png")))
        self.bttnDelEmp.setIconSize(QSize(64, 64))
        self.bttnDelEmp.clicked.connect(lambda: self.gotoPage("Del Employee"))

        self.bttnShowEmp = QPushButton("Show Employee")
        self.bttnShowEmp.setIcon(QIcon(QPixmap("Resources/show_user.png")))
        self.bttnShowEmp.setIconSize(QSize(64, 64))
        self.bttnShowEmp.clicked.connect(lambda: self.gotoPage("Show Employee"))


        self.bttnAddDesignation = QPushButton("Add Designation")
        self.bttnAddDesignation.setIcon(QIcon(QPixmap("Resources/add_designation.png")))
        self.bttnAddDesignation.setIconSize(QSize(64, 64))
        self.bttnAddDesignation.clicked.connect(lambda: self.gotoPage("Add Designation"))

        self.bttnEditDesg = QPushButton("Edit Designation")
        self.bttnEditDesg.setIcon(QIcon(QPixmap("Resources/edit_designation.png")))
        self.bttnEditDesg.setIconSize(QSize(64, 64))

        self.bttnDelDesg = QPushButton("Delete Designation")
        self.bttnDelDesg.setIcon(QIcon(QPixmap("Resources/delete_designation.png")))
        self.bttnDelDesg.setIconSize(QSize(64, 64))

        self.bttnShowDesg = QPushButton("Show Designations")
        self.bttnShowDesg.setIcon(QIcon(QPixmap("Resources/show_designation.png")))
        self.bttnShowDesg.setIconSize(QSize(64, 64))
        self.bttnShowDesg.clicked.connect(lambda: self.gotoPage("Show Designation"))


        self.bttnCalcSalary = QPushButton("Generate Payslip")
        self.bttnCalcSalary.setIcon(QIcon(QPixmap("Resources/rupee.png")))
        self.bttnCalcSalary.setIconSize(QSize(60, 60))
        self.bttnCalcSalary.clicked.connect(lambda: self.gotoPage("Calc Salary"))

        self.bttnSettings = QPushButton("Settings")
        self.bttnSettings.setIcon(QIcon(QPixmap("Resources/icons8-settings-96.png")))
        self.bttnSettings.setIconSize(QSize(55, 55))

        self.setupUI()

    def gotoPage(self, name):
        if self.__parent is not None:
            self.__parent.gotoPage(name)


    def setupUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)


        self.setContentsMargins(20, 10, 20, 5)

        bttnList = [self.bttnAddDesignation, self.bttnDelDesg, self.bttnEditDesg, self.bttnShowDesg,
                    self.bttnShowEmp, self.bttnEditEmp, self.bttnAddEmployee, self.bttnDelEmp,
                    self.bttnSettings, self.bttnCalcSalary]
        for bttn in bttnList:
            bttn.setObjectName("HomeBttn")
            bttn.setIconSize(QSize(55,55))

        employeeGroup = QGroupBox("Employee")
        employeeGroupLayout = QVBoxLayout()
        employeeGroupLayout.addWidget(self.bttnAddEmployee)
        employeeGroupLayout.addWidget(self.bttnEditEmp)
        employeeGroupLayout.addWidget(self.bttnDelEmp)
        employeeGroupLayout.addWidget(self.bttnShowEmp)
        employeeGroup.setLayout(employeeGroupLayout)

        designationGroup = QGroupBox("Designation")
        designationGroupLayout = QVBoxLayout()
        designationGroupLayout.addWidget(self.bttnAddDesignation)
        designationGroupLayout.addWidget(self.bttnEditDesg)
        designationGroupLayout.addWidget(self.bttnDelDesg)
        designationGroupLayout.addWidget(self.bttnShowDesg)
        designationGroup.setLayout(designationGroupLayout)

        groups = QHBoxLayout()
        groups.addWidget(employeeGroup)
        groups.addWidget(designationGroup)

        otherBttns = QGroupBox()
        otherBttnsLayout = QVBoxLayout()
        otherBttnsLayout.addWidget(self.bttnCalcSalary)
        otherBttnsLayout.addWidget(self.bttnSettings)
        otherBttnsLayout.addStretch()
        otherBttns.setLayout(otherBttnsLayout)
        groups.addWidget(otherBttns)

        groups.addStretch()

        layout.addLayout(groups)

        layout.addStretch()

        version = QLabel(version_text)
        layout.addWidget(version)

        centerLayout = QHBoxLayout()
        centerLayout.addStretch()
        centerLayout.addLayout(layout)
        centerLayout.addStretch()
        self.setLayout(centerLayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = HomeWidget()
    w.setStyleSheet(open("styleSheet/flatStyleSheet.css","r").read())
    w.show()

    sys.exit(app.exec_())
