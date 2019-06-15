from PySide import QtGui, QtCore


class ValidatingLineEdit(QtGui.QLineEdit):

    def __init__(self, fieldName, regex, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.fieldName = fieldName
        self.__edited = False

        if isinstance(regex, QtGui.QValidator):
            # self.setValidator(regex)
            self.__validator = regex
        else:
            if not isinstance(regex, QtCore.QRegExp):
                regex = QtCore.QRegExp(regex)
            # self.setValidator(QtGui.QRegExpValidator(regex))
            self.__validator = QtGui.QRegExpValidator(regex)

        self.textChanged.connect(self.__adjustColor)

        self.button = QtGui.QToolButton(self)
        self.button.setStyleSheet("QToolButton{background: transparent;}")
        self.button.setIconSize(QtCore.QSize(18, 18))

    def resizeEvent(self, *args, **kwargs):
        QtGui.QLineEdit.resizeEvent(self, *args, **kwargs)
        buttonSize = self.button.sizeHint()
        self.button.move(self.rect().right() - buttonSize.width(),
                         (self.rect().bottom() - buttonSize.height() + 1) / 2)

    def __adjustColor(self):
        self.__edited = True
        if self.isValid():
            self.setObjectName("valid")
            self.button.setIcon(QtGui.QIcon(QtGui.QPixmap("Resources/icons8-ok-48.png")))
        else:
            self.setObjectName("invalid")
            self.button.setIcon(QtGui.QIcon(QtGui.QPixmap("Resources/icons8-cancel-48.png")))
        self.setStyleSheet(self.styleSheet())

    def __toDefaultColor(self):
        self.setObjectName("default")
        self.button.setIcon(QtGui.QIcon())
        self.__edited = False

    def isValid(self):
        state, _, _ = self.__validator.validate(self.text(), len(self.text()))
        if state == QtGui.QValidator.Acceptable:
            return True
        return False

    def enterEvent(self, *args, **kwargs):
        QtGui.QLineEdit.enterEvent(self, *args, **kwargs)
        if self.__edited and not self.isValid():
            QtGui.QToolTip.showText(self.mapToGlobal(self.rect().topRight()), self.getErrorMessage(), self)

    def getErrorMessage(self):
        if self.isValid():
            return ""
        elif len(self.text()) == 0:
            return self.fieldName + " is required!"
        else:
            return "Invalid input for " + self.fieldName

    def setText(self, *args, **kwargs):
        QtGui.QLineEdit.setText(self, *args, **kwargs)
        self.__toDefaultColor()

    def clear(self, *args, **kwargs):
        QtGui.QLineEdit.clear(self, *args, **kwargs)
        self.__toDefaultColor()