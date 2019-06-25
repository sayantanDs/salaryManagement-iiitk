from PySide import QtGui, QtCore


class ReconnectMsg(QtGui.QWidget):
    """PySide widget that appears on screen to show the message - "Server connection lost! Reconnecting to server..."

    ReconnectMsg extends QWidget. It shows a frameless(No title bar or border) Widget at the center of screen
    with the message "Server connection lost! Reconnecting to server..." and an error icon.
    This widget does not attempt to connect or reconnect to server. The sole purpose of this widget is to
    show the message. The server connection is handled in DatabaseManager.

    """
    def __init__(self):
        QtGui.QWidget.__init__(self)

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
