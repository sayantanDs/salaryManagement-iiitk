from datetime import datetime

class Salary:
    def __init__(self, *args):
        if len(args) == 4:
            emp, desig, self.month, self.year = args
            self.year = int(self.year)
            self.__emp = emp
            self.id = emp.id
            self.originalPay = emp.originalPay
            self.originalPayGrade = emp.originalPayGrade
            self.designation, self.da_percent, self.hra_percent, self.ta_percent, self.it_percent, self.pt_percent = desig.toTuple()
            self.date = datetime(self.year, self.monthToNum(self.month), 1)
        else:
            self.id, self.date, self.designation, self.originalPay, self.originalPayGrade, \
            self.da_percent, self.hra_percent, self.ta_percent, self.it_percent, self.pt_percent = args
            self.month = self.numToMonth(self.date.month)
            self.year = self.date.year

        self.presentPay = self.originalPay + self.originalPayGrade
        self.da = (self.presentPay * self.da_percent) / 100
        self.hra = (self.presentPay * self.hra_percent) / 100
        self.ta = (self.presentPay * self.ta_percent) / 100
        self.it = (self.presentPay * self.it_percent) / 100
        self.pt = (self.presentPay * self.pt_percent) / 100

        self.grossEarnings = self.presentPay + self.da + self.hra + self.ta
        self.grossDeductions = self.it + self.pt
        self.netPay = self.grossEarnings - self.grossDeductions

    def result(self):
        return self.__emp.toTuple() + (
                self.da, self.hra, self.ta, self.it, self.pt, self.presentPay, self.grossEarnings, self.grossDeductions,
                self.netPay, self.month, self.year)

    def toTuple(self):
        return (self.id, self.date, self.designation, self.originalPay, self.originalPayGrade,
                self.da_percent, self.hra_percent, self.ta_percent, self.it_percent, self.pt_percent)

    def __iter__(self):
        t = self.toTuple()
        for x in t:
            yield x

    def monthToNum(self, month):
        m = {"JANUARY"  :   1,
             "FEBRUARY" :   2,
             "MARCH"    :   3,
             "APRIL"    :   4,
             "MAY"      :   5,
             "JUNE"     :   6,
             "JULY"     :   7,
             "AUGUST"   :   8,
             "SEPTEMBER":   9,
             "OCTOBER"  :   10,
             "NOVEMBER" :   11,
             "DECEMBER" :   12}
        return m[month]

    def numToMonth(self, n):
        m = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
        "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
        return m[n];