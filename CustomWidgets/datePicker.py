from PySide import QtCore, QtGui


class DatePicker(QtGui.QWidget):
    """PySide widget to select a date from a input box or from a calender that drops down on clicking a button

    DatePicker extends QWidget. It contains a QDateEdit input box where date may be entered manually.
    It also contains a QCalenderWidget that drops down on clicking a QPushButton. Selecting a date from the drop-down
    QCalenderWidget will automatically update the date in QDateEdit input box.

    Example::

        d = DatePicker()    # creates a DatePicker object
        date = d.getDate()   # returns the selected date

    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self._dateEdit = QtGui.QDateEdit()

        self._dateEdit.setDisplayFormat("dd/MM/yyyy")
        self._bttn = QtGui.QPushButton("")  # create a button with no text. Icon for this is set from stylesheet
        self._bttn.setObjectName("MenuBttn")

        menu = QtGui.QMenu(self._bttn)
        cal = QtGui.QCalendarWidget()
        action = QtGui.QWidgetAction(self._bttn)
        action.setDefaultWidget(cal)
        menu.addAction(action)
        self._bttn.setMenu(menu)
        cal.clicked[QtCore.QDate].connect(self._dateEdit.setDate)

        self.__setupUI()

    def setDate(self, date):
        """Sets the given date in the DatePicker

        Args:
            date (QDate):  this date is set in the DatePicker

        Returns:
            None

        """
        self._dateEdit.setDate(date)

    def getDate(self):
        """Returns the selected date

        Returns:
            QDate: The selected date

        """
        return self._dateEdit.date()

    def clear(self):
        self._dateEdit.findChild(QtGui.QLineEdit).setText('')

    def setReadOnly(self, val=True):
        self._dateEdit.findChild(QtGui.QLineEdit).setReadOnly(val)

    def __setupUI(self):
        self._bttn.setMaximumWidth(20)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._dateEdit)
        layout.addWidget(self._bttn)
        layout.addStretch()
        self.setLayout(layout)


