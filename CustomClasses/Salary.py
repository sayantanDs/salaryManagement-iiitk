from datetime import datetime

class Salary:
    """Class to represent and calculate Salary

    This class takes an Employee object, a Designation object (or all the designation info)
    and calculates the Salary for the given Employee for a given month and year
    """
    def __init__(self, *args):
        """

        Note:
            This function can take a variable number of arguments as it uses ``*args``.
            The special syntax ``*args`` in function definitions in python is used to pass
            a variable number of arguments to a function

            More info on variable number of arguments: https://www.geeksforgeeks.org/args-kwargs-python/

            Hence it is almost like having an overloaded constructor where multiple parameter lists are possible.

            This function supports two formats of arguments,  as listed below.
            The first one is used for calculating salary of an employee and storing it in database.
            Second one is used  to load stored salary from database and make a Salary object

            Valid argument lists:
                - emp: Employee object
                - desig: Designation object
                - month: month (from 1-12 or name of the month) for which salary is being calculated
                - year: year for which salary is being calculated

                OR

                - emp: Employee object
                - date: date containing month and year of salary calculation
                - designation: name of designation
                - originalPay: original pay
                - gradePay: original grade pay
                - da: Dearness Allowance percent
                - hra: House Rent Allowance percent
                - ta: Transport Allowance percent
                - it: Income Tax percent
                - pt: Profession Tax percent

        Args:
            *args: variable length argument list. Arguments should be given in one of the two formats mentioned above.

        """

        # process first type of argument list
        if len(args) == 4:
            emp, desig, self.month, self.year = args
            self.month = str(self.month)
            self.year = int(self.year)
            self.originalPay = emp.originalPay
            self.gradePay = emp.gradePay
            self.designation, self.da_percent, self.hra_percent, self.ta_percent, self.it_percent, self.pt_percent = desig.toTuple()
            self.date = self.monthYearToDate(self.month, self.year)

        # process second type of argument list
        else:
            emp = args[0]
            self.date = args[1]
            if isinstance(self.date, bytearray):
                self.date = datetime.strptime(str(self.date), '%Y-%m-%d')
            self.designation = str(args[2])
            self.originalPay, self.gradePay, \
            self.da_percent, self.hra_percent, self.ta_percent, self.it_percent, self.pt_percent = [float(x) for x in args[3:]]

            self.month, self.year = self.dateToMonthYear(self.date)

        self.id = emp.id
        self.name = emp.name
        self.doj = emp.doj
        self.pan = emp.pan

        # Calculate salary from available data
        self.presentPay = self.originalPay + self.gradePay
        self.da = (self.presentPay * self.da_percent) / 100
        self.hra = (self.presentPay * self.hra_percent) / 100
        self.ta = (self.presentPay * self.ta_percent) / 100
        self.grossEarnings = self.presentPay + self.da + self.hra + self.ta
        self.it = (self.grossEarnings * self.it_percent) / 100
        self.pt = (self.grossEarnings * self.pt_percent) / 100
        self.grossDeductions = self.it + self.pt
        self.netPay = self.grossEarnings - self.grossDeductions

        # rounding off
        self.presentPay = round(self.presentPay,3)
        self.originalPay = round(self.originalPay,3)
        self.da = round(self.da,3)
        self.hra = round(self.hra,3)
        self.ta = round(self.ta,3)
        self.grossEarnings = round(self.grossEarnings,3)
        self.it = round(self.it,3)
        self.pt = round(self.pt,3)
        self.grossDeductions = round(self.grossDeductions,3)
        self.netPay = round(self.netPay,3)

    def result(self):
        """Method to get salary info in format required by GUI

        Returns:
            The Salary info in a tuple arranged in the order required by the GUI
        """

        return (self.id, self.name, self.designation, '%.03f'%(self.originalPay), self.gradePay, self.doj, self.pan,
                '%.03f'%(self.da), '%.03f'%(self.hra), '%.03f'%(self.ta), '%.03f'%(self.it), '%.03f'%(self.pt), '%.03f'%(self.presentPay),
                '%.03f'%(self.grossEarnings), '%.03f'%(self.grossDeductions),
                '%.03f'%(self.netPay), self.month, self.year)

    def toTuple(self):
        """Method to get salary info in format required by DatabaseManager

        Unless DatabaseManager does some extra manipulations, this the order in which data is stored in the database

        Returns:
            The Salary info in a tuple arranged in the order required by the DatabaseManager

        """
        date_id = "%s,%02d/%04d" % (self.id, self.date.month, self.date.year)
        return (date_id, self.id, self.date, self.designation, self.originalPay, self.gradePay,
                self.da_percent, self.hra_percent, self.ta_percent, self.it_percent, self.pt_percent)

    def __iter__(self):
        t = self.toTuple()
        for x in t:
            yield x

    @staticmethod
    def monthYearToDate(month, year):
        return datetime(year, Salary.monthToNum(month), 1)

    @staticmethod
    def dateToMonthYear(date):
        return (Salary.numToMonth(date.month), date.year)

    @staticmethod
    def monthToNum(month):
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
        return m[str(month).upper()]

    @staticmethod
    def numToMonth(n):
        m = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
        "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
        return m[n]