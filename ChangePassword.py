from PySide import QtGui
import mysql.connector
from ShowMySqlError import ShowMysqlError
from DatabaseManager import Database


class ChangePasswordWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.__parent = parent
        
        self.title = "Change Password"

        self.currentpassword = QtGui.QLineEdit(self)
        self.currentpassword.setPlaceholderText("Current Password")
        self.currentpassword.setEchoMode(QtGui.QLineEdit.Password)

        self.newpassword = QtGui.QLineEdit(self)
        self.newpassword.setPlaceholderText("New password")
        self.newpassword.setEchoMode(QtGui.QLineEdit.Password)

        self.showPass = QtGui.QCheckBox("Show Password")
        self.showPass.stateChanged.connect(self.handleShowPassword)
        
        self.bttnLogin = QtGui.QPushButton("Change", self)
        self.bttnLogin.setObjectName("LoginButton")
        self.bttnLogin.clicked.connect(self.changePassword)
        self.newpassword.returnPressed.connect(self.changePassword)

        self.bttnCancel = QtGui.QPushButton("Cancel")
        self.bttnCancel.setObjectName("CancelButton")
        self.bttnCancel.clicked.connect(self.goBack)

        self.setupUI()

    def handleShowPassword(self):
        if self.showPass.isChecked():
            self.currentpassword.setEchoMode(QtGui.QLineEdit.Normal)
            self.newpassword.setEchoMode(QtGui.QLineEdit.Normal)
        else:
            self.currentpassword.setEchoMode(QtGui.QLineEdit.Password)
            self.newpassword.setEchoMode(QtGui.QLineEdit.Password)

    def changePassword(self):
        try:
            if Database.getdb().checkLogin(self.__parent.username, self.currentpassword.text()):
                Database.getdb().changeLogin(self.__parent.username, self.newpassword.text())
                if self.__parent is not None:
                    QtGui.QMessageBox(QtGui.QMessageBox.NoIcon, "Success", "Password changed successfully!",
                                      parent=self).exec_()
                    self.__parent.gotoPage("Home")
            else:
                QtGui.QMessageBox.warning(self, 'Error', 'Bad user or password! Password not changed!')
        except mysql.connector.Error as e:
            ShowMysqlError(e,self)

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def setupUI(self):

        layout = QtGui.QVBoxLayout()
        layout.addStretch(1)

        self.setContentsMargins(20, 10, 20, 5)

        loginGroup = QtGui.QGroupBox("Change Password")
        loginGroup.setObjectName("Login")
        loginGroup.setMinimumWidth(300)
        loginLayout = QtGui.QVBoxLayout()
        loginLayout.setContentsMargins(10, 10, 10, 30)
        form = QtGui.QFormLayout()

        form.addRow(QtGui.QLabel("Current Password"), self.currentpassword)
        form.addRow(QtGui.QLabel("New Password"), self.newpassword)
        loginLayout.addLayout(form)
        loginLayout.addSpacing(10)
        loginLayout.addWidget(self.showPass)
        loginLayout.addSpacing(30)

        bttnLayout = QtGui.QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnLogin)
        loginLayout.addLayout(bttnLayout)
        loginGroup.setLayout(loginLayout)

        hlayout = QtGui.QHBoxLayout()
        hlayout.addStretch()
        hlayout.addWidget(loginGroup)
        hlayout.addStretch()
        layout.addLayout(hlayout)
        layout.addStretch(2)

        bttnLayout = QtGui.QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnCancel)
        layout.addLayout(bttnLayout)

        self.setLayout(layout)


