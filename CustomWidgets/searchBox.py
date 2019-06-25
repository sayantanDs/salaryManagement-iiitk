from PySide import QtGui, QtCore
import sys


class SearchBox(QtGui.QComboBox):
    """PySide widget for search box with drop-down suggestions, extends QComboBox

    Creates an input box which shows suggestions based on the list passed in the init function
    Suggestion list can also be set using the setList() method.

    This can only be used when all possible inputs are known and available in a list.
    For example - a SearchBox for taking input for name of an employee working in an organization. In this case
    suggestion list would contain name of all employees. Now if user enters 'Ra', all the name beginning with 'Ra'
    will be shown in suggestion.

    This widget also contains a down arrow button on the right end. Clicking that will show a drop-down of
    all possible inputs and any one could be selected.

    A search button is also available (showing icon of magnifying glass). Clicking this button or pressing Enter key
    will emit returnPressed Signal with the current string in the search box. This signal can then be connected
    to required function.

    Example::

        def func(s):
            print "searching for", s

        suggestion_list = ["value 1", "value 2", "some other value"]
        w = SearchBox(None, suggestion_list)    # first argument is parent widget
        w.returnPressed.connect(func)

    Attributes:

        __textChangeStatus (bool): maintains record if text is changed since last search (or creation of widget).
            If text is not changed since last search, pressing enter or clicking search again
            will not emit returnPressed Signal. Hence preventing spamming of search.


    """

    returnPressed = QtCore.Signal(str)

    def __init__(self, parent=None, suggestionList=[]):
        """
        Args:
            parent (QWidget): parent widget of the SearchBox
                (default is None)
            suggestionList (list of strs): suggestion list to show suggestions from
                (default is [])
        """
        QtGui.QComboBox.__init__(self, parent)
        self.setEditable(True)
        self.setInsertPolicy(QtGui.QComboBox.NoInsert)

        if suggestionList is not None and len(suggestionList) > 0:
            self.setList(suggestionList)

        self.__textChangeStatus = True
        self.editTextChanged.connect(self.__onTextChange)
        self.currentIndexChanged.connect(self.__onIndexChange)
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self, self.__onEnter)
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self, self.__onEnter)

        self.button = QtGui.QToolButton(self)
        self.button.setIcon(QtGui.QIcon(QtGui.QPixmap("Resources/search.png")))
        self.button.setIconSize(QtCore.QSize(18, 18))
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.clicked.connect(self.__onEnter)
        self.setObjectName("searchBox")
        self.button.setObjectName("search")

    def resizeEvent(self, *args, **kwargs):
        QtGui.QComboBox.resizeEvent(self, *args, **kwargs)
        buttonSize = self.button.sizeHint()
        self.button.move(self.rect().right() - buttonSize.width() - 15,
                         (self.rect().bottom() - buttonSize.height() + 1) / 2)

    def __onTextChange(self):
        self.__textChangeStatus = True

    def __onIndexChange(self, index):
        if index >= 0:
            self.__onEnter()

    def __onEnter(self):
        # this function is called on pressing Enter or clicking search
        # it checks if text changed since last search. If it changed
        # it emits returnPressed signal and changes __textChangeStatus
        # back to False to prevent spamming of enter key

        if self.__textChangeStatus:
            print "Enter Pressed, text:", self.text()
            self.returnPressed.emit(self.text())
            self.__textChangeStatus = False

    def setPlaceholderText(self, text):
        self.findChild(QtGui.QLineEdit).setPlaceholderText(text)

    def text(self):
        return self.currentText()

    def setList(self, suggestionList):
        """Sets the suggestion list to show suggestions from

        Args:
            suggestionList (list of str): the list of suggestions to be shown

        Returns:
            None
        """

        self.clear()
        self.addItems(suggestionList)
        autoCompleteModel = QtGui.QStringListModel(suggestionList)
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