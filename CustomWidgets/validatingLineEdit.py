from PySide import QtGui, QtCore


class ValidatingLineEdit(QtGui.QLineEdit):

    def __init__(self, fieldName, regex, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.fieldName = fieldName

        if isinstance(regex, QtGui.QValidator):
            # self.setValidator(regex)
            self.__validator = regex
        else:
            if not isinstance(regex, QtCore.QRegExp):
                regex = QtCore.QRegExp(regex)
            # self.setValidator(QtGui.QRegExpValidator(regex))
            self.__validator = QtGui.QRegExpValidator(regex)

        self.textChanged.connect(self.__adjustColor)

    def __adjustColor(self):
        # if self.hasAcceptableInput():
        if self.isValid():
            self.setObjectName("valid")
        else:
            self.setObjectName("invalid")
        self.setStyleSheet(self.styleSheet())

    def isValid(self):
        state, _, _ = self.__validator.validate(self.text(), len(self.text()))
        if state == QtGui.QValidator.Acceptable:
            return True
        return False
        # return self.hasAcceptableInput()

    def getErrorMessage(self):
        if self.isValid():
            return ""
        elif len(self.text()) == 0:
            return self.fieldName + " is required!"
        else:
            return "Invalid input for " + self.fieldName

    def setText(self, *args, **kwargs):
        QtGui.QLineEdit.setText(self, *args, **kwargs)
        self.setObjectName("default")

    def clear(self, *args, **kwargs):
        QtGui.QLineEdit.clear(self, *args, **kwargs)
        self.setObjectName("default")