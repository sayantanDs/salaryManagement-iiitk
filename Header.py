from PySide import QtGui, QtCore


class Header(QtGui.QFrame):
    """PySide widget meant to stay at the top throughout the use of the application (thus called Header)

    This contains the organization logo, name, application name(Eg: 'Salary Management System' ) and a label for title.

    Note:

        Header title is  not to be confused with the text in titlebar, this title is just a text
        in this Header widget shown in big, prominent font meant to indicate which
        page(or view) the application is currently in.
        Say the application is at Add Employee page. So the title may be set to  'Add Employee'.

    """

    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.setObjectName("header")
        self.headerText = QtGui.QLabel()
        self.headerText.setObjectName("headerText")
        self.headerText2 = QtGui.QLabel()
        self.headerText2.setObjectName("headerText2")
        self.title = QtGui.QLabel()
        self.title.setObjectName("title")
        self.logo = QtGui.QLabel()
        # self.logo.setPixmap("Resources/iiitk.png")
        self.logo.setFixedSize(70, 70)
        self.logo.setScaledContents(True)
        self.setupUI()

    def setLogo(self, picPath):
        """Sets the logo to be displayed in Header

        Args:
            picPath (str): Path to the picture

        """
        self.logo.setPixmap(picPath)

    def setHeaderText(self, header1, header2=""):
        """Sets two lines of header text, usually application name and organization name

        Args:
            header1 (str):  First heading line
            header2 (str, optional):  Second heading line

        """
        self.headerText.setText(header1)
        self.headerText2.setText(header2)

    def setTitle(self, titleText =""):
        """Sets the title text in the Header

        Args:
            titleText (str): Title to be set
        """

        self.title.setText(titleText)

    def setupUI(self):
        banner = QtGui.QHBoxLayout()
        # banner.addStretch()
        banner.addWidget(self.logo)
        banner.setAlignment(QtCore.Qt.AlignCenter)
        bannerTextLayout = QtGui.QVBoxLayout()
        bannerTextLayout.setAlignment(QtCore.Qt.AlignCenter)
        bannerTextLayout.addWidget(self.headerText)
        bannerTextLayout.setAlignment(self.headerText, QtCore.Qt.AlignBottom)
        bannerTextLayout.addWidget(self.headerText2)
        bannerTextLayout.setAlignment(self.headerText2, QtCore.Qt.AlignTop)
        # bannerTextLayout.addWidget(self.title)
        banner.addLayout(bannerTextLayout)
        banner.addStretch()
        banner.addWidget(self.title)
        self.setLayout(banner)