from PySide import QtGui, QtCore
import sys

'''
Creates an input box which shows suggestions based on the list passed in the init function
Suggestion list can also be set using the setList() method
'''

class SearchBox(QtGui.QComboBox):
    returnPressed = QtCore.Signal(str)

    def __init__(self, parent=None, list=[]):
        QtGui.QComboBox.__init__(self, parent)
        self.setEditable(True)
        self.setInsertPolicy(QtGui.QComboBox.NoInsert)

        self.addItems(list)

        autoCompleteModel = QtGui.QStringListModel(list)
        completer = QtGui.QCompleter()
        completer.setModel(autoCompleteModel)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.setCompleter(completer)

        self.setEditText("")
        self.setCurrentIndex(-1)

        self.__textChangeStatus = True
        self.editTextChanged.connect(self.__onTextChange)
        self.currentIndexChanged.connect(self.__onIndexChange)
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self, self.__onEnter)
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self, self.__onEnter)

    def __onTextChange(self):
        self.__textChangeStatus = True

    def __onIndexChange(self, index):
        if index >= 0:
            self.__onEnter()

    def __onEnter(self):
        if self.__textChangeStatus:
            print "Enter Pressed, text:", self.text()
            self.returnPressed.emit(self.text())
            self.__textChangeStatus = False

    def setPlaceholderText(self, text):
        self.findChild(QtGui.QLineEdit).setPlaceholderText(text)

    def text(self):
        return self.currentText()

    def setList(self, list):
        self.clear()
        self.addItems(list)
        autoCompleteModel = QtGui.QStringListModel(list)
        completer = QtGui.QCompleter()
        completer.setModel(autoCompleteModel)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setCompleter(completer)
        self.setEditText("")
        self.setCurrentIndex(-1)


# for testing searchBox widget independently
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = SearchBox(None, ["hello", "hi"])
    w.show()
    sys.exit(app.exec_())