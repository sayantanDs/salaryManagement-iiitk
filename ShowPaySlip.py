from PySide.QtGui import QWidget, QApplication, QPushButton, QLabel,\
        QLineEdit, QComboBox, QHBoxLayout, QFormLayout, QVBoxLayout, QMessageBox, QFrame, QFileDialog, QSpinBox, QGroupBox
from printPaySlip import printPaySlip

class ShowPaySlipWidget(QWidget):
    def __init__(self,
                 parent,
                 emp,
                 desg,
                 month, year):
        QWidget.__init__(self)
        self.title = "Salary Result"
        # self.setGeometry(50, 50, 800, 600)

        self.__parent = parent

        year = int(year)

        presentPay = emp.originalPay + emp.originalPayGrade
        da = (presentPay * desg.da)/100
        hra = (presentPay * desg.hra) / 100
        ta = (presentPay * desg.ta) / 100
        it = (presentPay * desg.it) / 100
        pt = (presentPay * desg.pt) / 100

        grossEarnings = presentPay + da + hra + ta
        grossDeductions = it + pt
        netPay = grossEarnings - grossDeductions

        self.month = str(month)
        self.year = str(year)
        self.id = QLineEdit()
        self.id.setReadOnly(True)
        self.id.setText(emp.id)
        self.name = QLineEdit()
        self.name.setReadOnly(True)
        self.name.setText(emp.name)
        self.designation = QLineEdit()
        self.designation.setReadOnly(True)
        self.designation.setText(emp.designation)
        self.originalPay = QLineEdit()
        self.originalPay.setReadOnly(True)
        self.originalPay.setText(str(emp.originalPay))
        self.originalPayGrade = QLineEdit()
        self.originalPayGrade.setReadOnly(True)
        self.originalPayGrade.setText(str(emp.originalPayGrade))
        self.DOJ = QLineEdit()
        self.DOJ.setReadOnly(True)
        self.DOJ.setText(emp.getStrDate())
        self.pan = QLineEdit()
        self.pan.setReadOnly(True)
        self.pan.setText(emp.pan)

        self.presentPay = QLineEdit()
        self.presentPay.setReadOnly(True)
        self.presentPay.setText(str(presentPay))
        self.da = QLineEdit()
        self.da.setReadOnly(True)
        self.da.setText(str(desg.da))
        self.hra = QLineEdit()
        self.hra.setReadOnly(True)
        self.hra.setText(str(desg.hra))
        self.ta = QLineEdit()
        self.ta.setReadOnly(True)
        self.ta.setText(str(desg.ta))
        self.it = QLineEdit()
        self.it.setReadOnly(True)
        self.it.setText(str(it))
        self.pt = QLineEdit()
        self.pt.setReadOnly(True)
        self.pt.setText(str(desg.pt))

        self.grossAllowance = QLineEdit()
        self.grossAllowance.setReadOnly(True)
        self.grossAllowance.setText(str(grossEarnings))
        self.grossDeduction = QLineEdit()
        self.grossDeduction.setReadOnly(True)
        self.grossDeduction.setText(str(grossDeductions))

        self.netPay = QLineEdit()
        self.netPay.setReadOnly(True)
        self.netPay.setText(str(netPay))

        self.setupUI()


    def setupUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 10)
        layout.addWidget(QLabel("Salary for the month of %s, %s\n"%(self.month, self.year)))

        form1 = QFormLayout()
        form1.addRow(QLabel("ID No."), self.id)
        form1.addRow(QLabel("Name"), self.name)
        form1.addRow(QLabel("Designation"), self.designation)
        form1.addRow(QLabel("Original Pay"), self.originalPay)
        form1.addRow(QLabel("Original Pay Grade"), self.originalPayGrade)
        form1.addRow(QLabel("Date of joining"), self.DOJ)
        form1.addRow(QLabel("Pan No."), self.pan)

        infoGroup = QGroupBox("Basic Info")
        infoGroup.setLayout(form1)
        layout.addWidget(infoGroup)

        earningForm = QFormLayout()
        earningForm.addRow(QLabel("Present Pay"), self.presentPay)
        earningForm.addRow(QLabel("Dearness Allowance"), self.da)
        earningForm.addRow(QLabel("House Rent Allowance"), self.hra)
        earningForm.addRow(QLabel("Transport Allowance"), self.ta)
        earningForm.addRow(QLabel("Gross Earnings"), self.grossAllowance)

        leftGroup = QGroupBox("Allowances")
        leftGroup.setLayout(earningForm)


        deductionsForm = QFormLayout()
        deductionsForm.addRow(QLabel("Income Tax"), self.it)
        deductionsForm.addRow(QLabel("Profession Tax"), self.pt)
        deductionsForm.addRow(QLabel("Gross Deductions"), self.grossDeduction)

        rightGroup = QGroupBox("Deductions")
        rightGroup.setLayout(deductionsForm)

        table = QHBoxLayout()
        table.addWidget(leftGroup)
        table.addWidget(rightGroup)
        layout.addLayout(table)

        netPayLayout = QHBoxLayout()
        netPayLayout.addWidget(QLabel("Net Pay"))
        netPayLayout.addWidget(self.netPay)
        netPayLayout.addStretch()
        layout.addLayout(netPayLayout)

        self.bttnPrint = QPushButton("Print")
        self.bttnPrint.clicked.connect(self.printSlip)
        self.bttnCancel = QPushButton("Back")
        self.bttnCancel.clicked.connect(self.goBack)
        self.bttnPrint.setObjectName("OkButton")
        self.bttnCancel.setObjectName("CancelButton")

        layout.addStretch()
        bttnLayout = QHBoxLayout()
        bttnLayout.addStretch()
        bttnLayout.addWidget(self.bttnCancel)
        bttnLayout.addWidget(self.bttnPrint)

        layout.addLayout(bttnLayout)
        self.setLayout(layout)

    def goBack(self):
        if self.__parent is not None:
            self.__parent.goBack()

    def printSlip(self):
        printPaySlip(self.id.text(), self.name.text(), self.designation.text(),
                        float(self.originalPay.text()), float(self.originalPayGrade.text()), self.DOJ.text(),
                        self.pan.text(), float(self.da.text()), float(self.hra.text()), float(self.ta.text()),
                        float(self.it.text()), float(self.pt.text()), float(self.presentPay.text()),
                        float(self.grossAllowance.text()), float(self.grossDeduction.text()), float(self.netPay.text()),
                        self.month, int(self.year))