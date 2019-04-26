from PySide import QtCore, QtGui

'''
DatePicker is a widget to select a date from a QDateEdit Input box
or from a QCalenderWidget that drops down on clicking a button

getDate() returns the selected date
'''

class DatePicker(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self._dateEdit = QtGui.QDateEdit()

        self._dateEdit.setDisplayFormat("dd/MM/yyyy")
        self._bttn = QtGui.QPushButton("")
        self._bttn.setObjectName("MenuBttn")

        menu = QtGui.QMenu(self._bttn)
        cal = QtGui.QCalendarWidget()
        action = QtGui.QWidgetAction(self._bttn)
        action.setDefaultWidget(cal)
        menu.addAction(action)
        self._bttn.setMenu(menu)
        cal.clicked[QtCore.QDate].connect(self._dateEdit.setDate)

        self.setupUI()

    def setDate(self, date):
        self._dateEdit.setDate(date)

    def getDate(self):
        return self._dateEdit.date()

    def clear(self):
        self._dateEdit.findChild(QtGui.QLineEdit).setText('')

    def setReadOnly(self, val=True):
        self._dateEdit.findChild(QtGui.QLineEdit).setReadOnly(val)

    def setupUI(self):
        self._bttn.setMaximumWidth(20)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._dateEdit)
        layout.addWidget(self._bttn)
        layout.addStretch()
        self.setLayout(layout)


