from PySide import QtGui
from PySide.QtCore import QRegExp
import sys
import mysql.connector
from ShowMySqlError import ShowMysqlError
from DatabaseManager import Database

class LoginWidget(QtGui.QDialog):
    """A PySide widget that has GUI for performing Login

    This has two ``QLineEdit`` widgets. One for username and another for password. The password text is not shown
    by default. Checking the show password checkbox, shows the password text.
    On clicking 'Login' button, the given username and password are sent to the ``checkLogin`` method from
    DatabaseManager module. If this returns True, this widget opens the Home page, otherwise, a Dialog box
    is shown saying the given username or password was wrong.

    See Also:
        - :py:meth:`checkLogin() <DatabaseManager.databaseManager.DatabaseManager.checkLogin>` method from DatabaseManager module

    """
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)

        self._parent = parent
        self.title = "Log in"

        self.username = QtGui.QLineEdit(self)
        self.username.setPlaceholderText("Enter username")

        self.password = QtGui.QLineEdit(self)
        self.password.setPlaceholderText("Enter password")
        self.password.setEchoMode(QtGui.QLineEdit.Password)

        reg_ex = QRegExp("[a-zA-Z0-9-_]+")
        username_validator = QtGui.QRegExpValidator(reg_ex, self.username)
        self.username.setValidator(username_validator)

        self.password.returnPressed.connect(self.doLogin)

        self.showPass = QtGui.QCheckBox("Show Password")
        self.showPass.stateChanged.connect(self.handleShowPassword)
        self.bttnLogin = QtGui.QPushButton("Login", self)
        self.bttnLogin.setObjectName("LoginButton")
        self.bttnLogin.clicked.connect(self.doLogin)

        self.setupUI()

    def handleShowPassword(self):
        if self.showPass.isChecked():
            self.password.setEchoMode(QtGui.QLineEdit.Normal)
        else:
            self.password.setEchoMode(QtGui.QLineEdit.Password)

    def doLogin(self):
        try:
            # if DatabaseManager.db.checkLogin(self.username.text(), self.password.text()):
            if Database.getdb().checkLogin(self.username.text(), self.password.text()):
                if self._parent is not None:
                    self._parent.gotoPage("Home")
            else:
                QtGui.QMessageBox.warning(self, 'Error', 'Bad user or password')
        except mysql.connector.Error as e:
            ShowMysqlError(e,self)

    def setupUI(self):

        layout = QtGui.QVBoxLayout()
        layout.addStretch(1)

        self.setContentsMargins(20, 10, 20, 5)

        loginGroup = QtGui.QGroupBox("Login")
        loginGroup.setObjectName("Login")
        loginGroup.setMinimumWidth(300)
        loginLayout = QtGui.QVBoxLayout()
        loginLayout.setContentsMargins(10, 10, 10, 30)
        form = QtGui.QFormLayout()

        form.addRow(QtGui.QLabel("Username"), self.username)
        form.addRow(QtGui.QLabel("Password"), self.password)
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
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    w = LoginWidget()
    w.show()

    sys.exit(app.exec_())

