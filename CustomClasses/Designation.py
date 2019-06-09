class Designation:
    def __init__(self, designation, da, hra, ta, it, pt):
        self.designation = designation
        self.da = float(da)
        self.hra = float(hra)
        self.ta = float(ta)
        self.it = float(it)
        self.pt = float(pt)

    def toTuple(self):
        return (self.designation, self.da, self.hra, self.ta, self.it, self.pt)

    def __iter__(self):
        t = self.toTuple()
        for x in t:
            yield x