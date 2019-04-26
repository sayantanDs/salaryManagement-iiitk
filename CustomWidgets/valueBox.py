from PySide import QtGui


class ValueBox(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.value = QtGui.QLineEdit()
        self.value.setReadOnly(True)
        self.bttn = QtGui.QPushButton("Change")
        self.bttn.clicked.connect(self.onChange)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.value)
        layout.addWidget(self.bttn)
        self.setLayout(layout)

    def onChange(self):
        if self.value.text() != "":
            defaultFloat = float(self.value.text())

            num, ok = QtGui.QInputDialog.getDouble(self, "Input", "Enter new value:",defaultFloat , min=0, max=2147483647, decimals=3)
            if ok:
                self.value.setText(str(num))

    def clear(self):
        self.value.clear()

    def setText(self, text):
        self.value.setText(text)

    def text(self):
        return self.value.text()