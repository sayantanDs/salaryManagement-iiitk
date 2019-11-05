from PySide import QtCore
from datetime import datetime


class Employee:
    """A class to represent an Employee

    Stores all necessary details of an employee and performs any data type conversions if required.
    The DOJ received from GUI is in QDate format whereas date to be stored in Database needs it in python's
    datetime format. This conversion is taken care of internally by this class.

    toTuple() method returns the employee info in a tuple arranged in the order required by the DatabaseManager
    (unless DatabaseManager does some extra manipulations, this is the order in which data is stored in the database)

    """

    def __init__(self, id, name, designation, originalPay, originalPayGrade, doj, pan):
        """
        Args:
            id (str): ID of the employee
            name (str): Name of the employee
            designation (str): The designation of the employee
            originalPay: original pay
            originalPayGrade: original grade pay
            doj: Date of joining of the employee
            pan: PAN number of the employee

        Note:
            doj is stored internally in  python's datetime format. Hence if it is received as a QDate,
            it is converted to datetime first.

        """

        self.id = str(id)
        self.name = str(name)
        self.designation = str(designation)
        self.originalPay = float(originalPay)
        self.originalPayGrade = float(originalPayGrade)
        self.doj = doj
        if isinstance(doj, bytearray):
            self.doj = datetime.strptime(str(self.doj), '%Y-%m-%d')
        if isinstance(doj, QtCore.QDate):
            self.doj = datetime(self.doj.year(), self.doj.month(), self.doj.day())
        self.pan = str(pan)

    def toTuple(self):
        """Method to get employee info in format required by DatabaseManager

        Unless DatabaseManager does some extra manipulations, this the order in which data is stored in the database

        Returns:
            The employee info in a tuple arranged in the order required by the DatabaseManager

        """
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