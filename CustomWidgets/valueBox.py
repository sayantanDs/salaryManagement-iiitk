from PySide import QtGui


class ValueBox(QtGui.QWidget):
    """PySide widget with a line edit and a 'change' button clicking which gives an option to change line edit content

    ValueBox extends QWidget. It contains a QLineEdit which is set to read only (hence making it like a display box).
    Next to this there is a QPushButton with 'Change' written on it. Clicking this will open an input dialog box.
    This dialog box is created using QInputDialog.getDouble() and hence only accepts double as input.

    This widget is to be used to display double values and giving an option to change it upon clicking the button.

    """

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.value = QtGui.QLineEdit()
        self.value.setReadOnly(True)
        self.bttn = QtGui.QPushButton("Change")
        self.bttn.clicked.connect(self.__onChange)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.value)
        layout.addWidget(self.bttn)
        self.setLayout(layout)

    def __onChange(self):
        if self.value.text() != "":
            defaultFloat = float(self.value.text())

            num, ok = QtGui.QInputDialog.getDouble(self, "Input", "Enter new value:", defaultFloat,
                                                   min=0, max=2147483647, decimals=3)
            if ok:
                self.value.setText(str(num))

    def clear(self):
        self.value.clear()

    def setText(self, text):
        self.value.setText(text)

    def text(self):
        return self.value.text()