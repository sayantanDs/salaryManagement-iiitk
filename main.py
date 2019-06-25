from PySide import QtGui, QtCore
import sys

import mysql.connector

from DatabaseManager import Database

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
    """This is the Main Window inside which everything happens

    This application needs to have various pages for various tasks. For example it needs a page for adding employee, one
    for editing, one for deleting, one for Salary calculation, etc. Each of these pages are individually created by
    extending ``QWidget``. We also need to be able to jump from one page to other or go back to previous page easily.

    The trick used to achieve this easily can be understood with a simple example.
    Lets say we have two classes Apple and Banana. We need to create an instance of
    any one of them as required. We can do the following::

        fruits = { "apple" : Apple, "banana" : Banana }

        # we can get an Apple instance by writing -
        a = fruits["apple"]()   # same as writing a = Apple()
                                # as fruits["apple"] is substituted with Apple

        # We can take this further by putting it in a function -
        def make_fruit(name):
            return fruits[name]()   # This would return an instance of required fruit

        a = make_fruit("apple") # Returns an Apple object
        b = make_fruit("banana") # Returns a Banana object

    So all the classes for the pages are stored in a dictionary with a page name string as their key.
    So passing the page name to the dictionary will return an instance required page class. A ``gotoPage()`` method
    is made to take the page name and show corresponding page.

    Now the problem of dynamically creating an instance of required page is solved
    but we still need to be able to smoothly switch from one page to other.
    This is done using ``QStackedWidget`` which is like a stack of ``QWidgets`` that we can switch through.

    A ``goBack()`` method is made which goes back to previous page and deletes the current page instance.

    The central widget for the ``QMainWindow``is set to a blank widget which contains a ``Header`` widget at the top
    and a ``QStackedWidget`` ofr the rest of it.

    See Also:
        - :py:mod:`Header` module

    """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle("Salary Manager")
        self.setGeometry(50,50, 900, 700)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.setWindowIcon(QtGui.QIcon("Resources/rupee.png"))

        self.bgWidget = QtGui.QWidget()
        self.header = Header()
        self.header.setLogo("Resources/iiitk.png")
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

    def gotoPage(self, name, *args):
        """A method to open page corresponding to given name

        This method takes the page ``name`` and passes it to the pages dictionary to get corresponding class and
        creates a new instance of the class. The ``*args`` (if any) are passed to the constructor of that class.
        This newly created page is then added to the ``QStackedWidget`` and this new page is set as current page.

        As all pages are initialized in this class, this class is passed as an argument in the constructor
        and stored in __parent attribute. So, now we can use ``self.__parent.gotoPage()`` to access
        this ``gotoPage()`` from any class. Thus we now have the ability to go from any page to any page.
        Also, similarly they can use ``self.__parent.goBack()`` to access ``goBack()`` method of this class.

        Args:
            name (str): Name of the page
            *args: variable length argument list

        """
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
        """Method to go back to previous page

        This method sets the index of ``QWidgetStack`` used in this class to ``currentIndex - 1`` (hence effectively
        going to previous page). It then removes the previous page from the stack and deletes it.
        """
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
        """Sets the title text in the Header by calling setTile() method of the header

        Args:
            titleText (str): Title to be set

        See Also:
            :py:meth:`setTitle() <Header.Header.setTitle>` method of Header module

        """
        self.header.setTitle(titleText)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    try:

        splash_pix = QtGui.QPixmap("Resources/splash.png")
        splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        app.processEvents()

        # Database.connect(host="localhost",
        #                  databaseName="salaryManagement_test_1",
        #                  username="root",
        #                  password="root")

        Database.connect(host="remotemysql.com",
                         username="41Ng5H2E1B",
                         password="nGQNpBrowE",
                         databaseName="41Ng5H2E1B")

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


