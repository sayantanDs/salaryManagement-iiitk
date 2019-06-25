from PySide import QtGui, QtCore



class HomeWidget(QtGui.QWidget):
    """PySide widget for home page

    This will have Buttons to open all other pages of this application. All thesse buttons are supposed to have
    an icon, a text, and call ``gotoPage()`` method with correct page name when clicked. To make this repetitive task
    simpler a modified ``QPushButton`` called ``NavButton`` was made.
    """
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
        """Goes to the specified page

        Args:
            name (str): Name of the page

        Note:
            The pages (or views, which are essentially ``QWidgets``) are initialized in ``MainWindow`` class of
            ``main`` module. They are put in a dictionary with corresponding page names. The ``MainWindow`` class has
            the actual ``gotoPage()`` method to jump from one page to other. The ``gotoPage()`` in Home widget
            just calls that ``gotoPage()`` method from ``MainWindow`` class.

            (As all pages are intialized in ``MainWindow`` class, including Home, so they all have ``MainWindow`` class
            as their parent. This parent instance is passed in the constructor and stored in __parent attribute.
            Hence now we can use ``self.__parent.gotoPage()`` to access ``gotoPage()`` from ``MainWindow`` class.)

        See Also:
            - :py:meth:`gotoPage() <main.MainWindow.gotoPage>` method from :py:mod:`main` module

        """
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
        """Makes a ``QPushButton`` with given image, text and connects ``gotoPage()`` method with given page name

        Args:
            text (str): Text shown on the button
            img  (str): Path to image file
            page (str): Name of page which needs to opened on clicking this button
            parent (QWidget): Widget where this is placed
        """
        QtGui.QPushButton.__init__(self, text, parent=parent)
        self.setIcon(QtGui.QIcon(QtGui.QPixmap(img)))
        if page is not None:
            self.clicked.connect(lambda: parent.gotoPage(page))
