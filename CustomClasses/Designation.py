class Designation:
    """A class used to represent Designation of Employees

    Stores all the necessary details of a designation needed for salary calculation, such as allowances and deductions

    toTuple() method returns the designation info in a tuple arranged in the order required by the DatabaseManager
    (unless DatabaseManager does some extra manipulations, this is the order in which data is stored in the database)
    """

    def __init__(self, designation, da, hra, ta, it, pt):
        """
        Args:
            designation: Name of the designation
            da: Dearness Allowance
            hra: House Rent Allowance
            ta: Transport Allowance
            it: Income Tax
            pt: Profession Tax

        Note:
            The above arguments are taken as percentages, hence da = 123.45 would mean 123.45% of the basic pay

        """

        self.designation = str(designation)
        self.da = float(da)
        self.hra = float(hra)
        self.ta = float(ta)
        self.it = float(it)
        self.pt = float(pt)

    def toTuple(self):
        """Method to get designation info in format required by DatabaseManager

        Unless DatabaseManager does some extra manipulations, this the order in which data is stored in the database

        Returns:
            The designation info in a tuple arranged in the order required by the DatabaseManager
        """
        return (self.designation, self.da, self.hra, self.ta, self.it, self.pt)


    def __iter__(self):
        t = self.toTuple()
        for x in t:
            yield x