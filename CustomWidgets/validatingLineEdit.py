from PySide import QtGui, QtCore


class ValidatingLineEdit(QtGui.QLineEdit):
    """PySide widget to show visual feedback if input is valid/invalid, extends QLineEdit

    A modified QLineEdit which changes to a certain color on getting a valid input and
    another on getting invalid input. This class doesn't explicitly change colors, it just sets the object name
    to 'valid', 'invalid' or 'default'. The required colors are to be mentioned in the stylesheet using
    these object names. See https://doc.qt.io/archives/qt-4.8/stylesheet-syntax.html for more on stylesheets.

    A tooltip is shown on hovering on the widget after giving a wrong input.

    A 'tick' or 'cross' icon is displayed on the right end of the QLineEdit to clearly indicate valid or invalid input,
    just in case the colors are not properly visible.

    Examples:

        To create a ValidatingLineEdit for name, that will take only letters from a-z A-Z and space::

            nameBox = ValidatingLineEdit("Name", "[a-zA-Z\s]+")

        To create a ValidatingLineEdit for that will take double::

            payBox = ValidatingLineEdit("Pay", QtGui.QDoubleValidator())

        To check if input is valid, use::

            if nameBox.isValid():
                print "Valid"
            else:
                print "Invalid!"


    Attributes:

        __edited (bool): To keep track if input has been edited from initial value. The valid/invalid
            checking will only take place if  text is edited.
        __validator (QValidator): validator used to check if input is valid or not

    """

    def __init__(self, fieldName, regex, parent=None):
        """
        Args:
            fieldName (str): Name of the field for which input is being taken through this QLineEdit. This field name
                    might be shown in error messages.
            regex (str or QRegExp or QValidator): Regex or QValidator used to check if input is valid or not
            parent (QWidget): parent widget (optional)
                (default is None)

        """

        QtGui.QLineEdit.__init__(self, parent)
        self.fieldName = fieldName
        self.__edited = False

        if isinstance(regex, QtGui.QValidator):
            self.__validator = regex
        else:
            if not isinstance(regex, QtCore.QRegExp):
                regex = QtCore.QRegExp(regex)
            self.__validator = QtGui.QRegExpValidator(regex)

        self.textChanged.connect(self.__adjustColor)

        # A QToolButton is used to display the 'cross' or 'tick' icon
        self.button = QtGui.QToolButton(self)
        self.button.setStyleSheet("QToolButton{background: transparent;}")
        self.button.setIconSize(QtCore.QSize(18, 18))

    def resizeEvent(self, *args, **kwargs):
        QtGui.QLineEdit.resizeEvent(self, *args, **kwargs)
        # The QToolButton is moved to the right hand end of the QLineEdit
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
        self.button.setIcon(QtGui.QIcon())  # a blank icon is set
        self.__edited = False

    def isValid(self):
        state, _, _ = self.__validator.validate(self.text(), len(self.text()))
        if state == QtGui.QValidator.Acceptable:
            return True
        return False

    def enterEvent(self, *args, **kwargs):
        QtGui.QLineEdit.enterEvent(self, *args, **kwargs)
        # Show tooltip if input is invalid
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
        # setText is overrided to set QLineEdit to default color after setText
        p = self.cursorPosition()   # cursor Position is recorded
        QtGui.QLineEdit.setText(self, *args, **kwargs)  # original setText is called
        self.setCursorPosition(p)   # cursor is set to previous recorded position
        self.__toDefaultColor()     # QLineEdit is set to default color

    def clear(self, *args, **kwargs):
        QtGui.QLineEdit.clear(self, *args, **kwargs)
        self.__toDefaultColor()