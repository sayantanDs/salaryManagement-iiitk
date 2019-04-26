from PySide import QtGui


def ShowMysqlError(e, parent=None):
    m = str(e)
    if e.errno == 2003:
        m = "Unable to connect server! Please check your connection!"
    elif e.errno == 1062:
        m = "Unable to add duplicate entry! Please check the data and try again!"

    else:
        m = "Unknown error occured! Please check details for more info"

    msg = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Error", m, parent=parent)
    msg.setDetailedText(str(e))
    msg.exec_()