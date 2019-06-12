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

    @staticmethod
    def dateToStr(doj):
        return "%02d/%02d/%04d" % (doj.day, doj.month, doj.year)

    def getStrDate(self):
        return Employee.dateToStr(self.doj)

    def getQDate(self):
        return QtCore.QDate(self.doj.year, self.doj.month, self.doj.day)