from PySide import QtCore
from datetime import datetime


class Employee:
    def __init__(self, id, name, designation, originalPay, originalPayGrade, doj, pan):
        self.id = id
        self.name = name
        self.designation = designation
        self.originalPay = float(originalPay)
        self.originalPayGrade = float(originalPayGrade)
        self.doj = doj
        if isinstance(doj, QtCore.QDate):
            self.doj = datetime(self.doj.year(), self.doj.month(), self.doj.day())
        self.pan = pan

    def toTuple(self):
        return (self.id, self.name, self.designation, self.originalPay, self.originalPayGrade, self.doj, self.pan)

    def __iter__(self):
        t = self.toTuple()
        for x in t:
            yield x

    def getStrDate(self):
        return "%02d/%02d/%04d" % (self.doj.day, self.doj.month, self.doj.year)

    def getQDate(self):
        return QtCore.QDate(self.doj.year, self.doj.month, self.doj.day)