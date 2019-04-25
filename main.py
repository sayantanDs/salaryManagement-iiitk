from PySide import QtGui, QtCore
import sys



class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle("Salary Manager")
        self.setGeometry(50,50, 900, 700)
        self.setWindowState(QtCore.Qt.WindowMaximized)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())