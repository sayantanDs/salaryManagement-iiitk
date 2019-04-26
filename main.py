from PySide import QtGui, QtCore
import sys

import mysql.connector

import DatabaseManager

from Home import HomeWidget
from AddEmployee import AddEmployeeWidget
from DelEmployee import DelEmployeeWidget
from EditEmployee import EditEmployeeWidget
from ShowEmployee import ShowEmployeeWidget
from AddDesignation import AddDesignationWidget
from ShowDesignation import ShowDesigationWidget
from EditDesignation import EditDesignationWidget
from CalculateSalary import CalculateSalaryWidget
from ShowPaySlip import ShowPaySlipWidget
from Login import LoginWidget
from Header import Header

from ShowMySqlError import ShowMysqlError

# import resources

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle("Salary Manager")
        self.setGeometry(50,50, 900, 700)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.setWindowIcon(QtGui.QIcon("Resources/rupee.png"))

        self.bgWidget = QtGui.QWidget()
        self.header = Header()
        self.header.setHeaderText("Salary Management System", "Indian Institute of Information Technology Kalyani")

        self.widgetStack = QtGui.QStackedWidget()
        self.setCentralWidget(self.bgWidget)
        self.setupUI()

        self.pages = {
            "Login": LoginWidget,
            "Home": HomeWidget,
            "Add Employee": AddEmployeeWidget,
            "Del Employee": DelEmployeeWidget,
            "Edit Employee": EditEmployeeWidget,
            "Show Employee": ShowEmployeeWidget,
            "Add Designation": AddDesignationWidget,
            "Edit Designation": EditDesignationWidget,
            "Show Designation": ShowDesigationWidget,
            "Calc Salary": CalculateSalaryWidget,
            "Result": ShowPaySlipWidget
        }

        self.gotoPage("Login")

    def gotoPage(self, name, args=()):
        print "Goto page", name, ";   args=", args
        try:
            if len(args) == 0:
                newPage = self.pages[name](self)
            else:
                newPage = self.pages[name](self, *args)
            self.widgetStack.addWidget(newPage)
            self.widgetStack.setCurrentWidget(newPage)
            try:
                self.setTitle(newPage.title)
            except AttributeError as e:
                self.setTitle("")

        except mysql.connector.Error as e:
            ShowMysqlError(e, self)

    def goBack(self):
        print "Going Back"
        try:
            currentIndex = self.widgetStack.currentIndex()
            if currentIndex > 0:
                currentPage = self.widgetStack.currentWidget()
                self.widgetStack.setCurrentIndex(currentIndex-1)
                try:
                    self.setTitle(self.widgetStack.currentWidget().title)
                except AttributeError as e:
                    self.setTitle("")

                currentPage.deleteLater()
                self.widgetStack.removeWidget(currentPage)

        except mysql.connector.Error as e:
            ShowMysqlError(e, self)

    def setupUI(self):
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        layout.addWidget(self.header)
        layout.addWidget(self.widgetStack)

        self.bgWidget.setLayout(layout)

    def setTitle(self, titleText =""):
        self.header.setTitle(titleText)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    try:

        splash_pix = QtGui.QPixmap("Resources/splash.png")
        splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        app.processEvents()

        # DatabaseManager.db = DatabaseManager.DatabaseManager(host="localhost",
        #                                                      databaseName="salaryManagement_test_1",
        #                                                      username="root",
        #                                                      password="root")

        DatabaseManager.db = DatabaseManager.DatabaseManager(host="sql12.freemysqlhosting.net",
                                                             username="sql12287494",
                                                             password="ctR2K5xhG2",
                                                             databaseName="sql12287494")

        w = MainWindow()

        styleSheetFile = QtCore.QFile("styleSheet/flatStyleSheet.css")
        styleSheetFile.open(QtCore.QIODevice.ReadOnly)
        w.setStyleSheet(str(styleSheetFile.readAll()))

        w.show()

        splash.finish(w)

    except mysql.connector.Error as e:
        splash.close()
        ShowMysqlError(e)
        sys.exit()

    # except Exception as e:
    #     splash.close()
    #     msg = QMessageBox(QMessageBox.Critical, "Error", "Unexpected error occured!\n" + str(e))
    #     msg.exec_()
    #     sys.exit()

    sys.exit(app.exec_())


