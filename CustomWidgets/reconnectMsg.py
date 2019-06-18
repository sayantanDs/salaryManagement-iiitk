from PySide import QtGui, QtCore


class ReconnectMsg(QtGui.QFrame):
    def __init__(self):
        QtGui.QFrame.__init__(self)

        v = QtGui.QVBoxLayout()
        h = QtGui.QHBoxLayout()
        cross = QtGui.QLabel()
        cross.setPixmap(QtGui.QPixmap("Resources/icons8-cancel-48.png").scaledToWidth(32))
        h.addWidget(cross)
        h.addWidget(QtGui.QLabel("Server connection lost! Reconnecting to server..."))
        v.addLayout(h)
        v.setAlignment(QtCore.Qt.AlignHCenter)
        self.setLayout(v)

        self.setWindowFlags(QtCore.Qt.ToolTip)

        self.setFixedSize(300, 100)
        self.move(QtGui.QApplication.desktop().screen().rect().center() -
                  self.rect().center())
