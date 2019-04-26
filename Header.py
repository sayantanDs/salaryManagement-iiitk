from PySide import QtGui, QtCore

class Header(QtGui.QFrame):
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
        self.logo.setPixmap("Resources/iiitk.png")
        self.logo.setFixedSize(70, 70)
        self.logo.setScaledContents(True)
        self.setupUI()

    def setHeaderText(self, header1, header2 = ""):
        self.headerText.setText(header1)
        self.headerText2.setText(header2)

    def setTitle(self, titleText =""):
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