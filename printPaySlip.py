from PySide import QtGui, QtCore
import sys

def printPaySlip(id,
                name,
                designation,
                originalPay,
                originalPayGrade,
                DOJ,
                pan,
                da, hra, ta, incomeTax, professionTax,
                presentPay, totalEarnings, totalDeductions,
                netPay,
                month, year):

    htmlText = \
        '''
        <html>
        <body>
            <table>
                <tr>
                      <td align="center" style="padding: 0pt"><img src="{}" width="108"></td>
                      <td align="center" style="padding: 0pt">
                            <p align="center" style="font-size: 11pt; font-family:times">
                                <b>INDIAN INSTITUTE OF INFORMATION TECHNOLOGY</b>
                            </p>
                            <p align="center" style="font-size: 10pt; font-family:times">
                                (Autonomous Institute under MHRD, Govt. of India
                                <br>
                                & Department of Information Technology & Electronics, Govt. of West Bengal)
                                <br>
                                C/o WEBEL IT Park, Opposite Water Treatment Plant
                                <br>
                                Near Buddha Park, Dist-Nadia, P.O-Kalyani, PIN-741235,
                                <br>            
                                Email-ID iiitkalyani.office@gmail.com Website www.iiitkalyani.ac.in
                            </p>
                      </td>
                </tr>
            </table>
            <hr>
            <p align="center" style="font-size: 12pt; font-family:times">
                    <br>
                    <b>Salary for the month of {}, {}</b>
            </p>

            <br>
            <p style="font-size: 10pt; font-family:times">
            <table>
                <tr> <td>ID No.</td> <td> : </td> <td> {} </td> </tr>
                <tr> <td>Name</td> <td> : </td> <td> {} </td> </tr>
                <tr> <td>Designation</td> <td> : </td> <td> {} </td> </tr>
                <tr> <td>Original Pay</td> <td> : </td> <td> {} </td> </tr>
                <tr> <td>Original Grade Pay</td> <td> : </td> <td> {} </td> </tr>
                <tr> <td>Date of joining</td> <td> : </td> <td> {} </td> </tr>
                <tr> <td>Pan No.</td> <td> : </td> <td> {} </td> </tr>                
            </table>
            </p>

            <br><br>
            <p style="font-size: 10pt; font-family:times;">
            
            <table width=100%>
            <tr> <td colspan="4"><hr></td></tr>
            <tr> <th colspan="2" width=50%> EARNINGS </th> <th colspan="2"> DEDUCTIONS </th> </tr>
            <tr> <td colspan="4"><hr></td></tr>
                                   
            <tr> <td>Present Pay</td> <td> {} </td> <td> Income Tax </td><td>{}</td>  </tr>
            <tr> <td>Dearness Allowance</td> <td> {} </td> <td> Profession Tax</td><td> {}</td>  </tr>
            <tr> <td>House Rent Allowance</td> <td> {} </td> <td> </td><td> </td></tr>
            <tr> <td>Transport Allowance</td> <td> {} </td> <td> </td><td> </td></tr>
            <tr> <td colspan="4"><br><hr></td></tr>

                     
            <tr> <td>Gross Earnings</td> <td> {} </td> <td> Gross Deductions</td><td> {}</td></tr>
            <tr> <td colspan="4"><hr></td></tr>
            <tr> <td></td> <td></td> <td> Net Pay </td><td> {}</td></tr>
            <tr> <td colspan="4"><hr></td></tr>
            </table>
            </p>

            <p align="right" style="font-size: 10pt; font-family:times;">
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            Assistant Registrar (Finance)
            </p>

        </body>
        </html>
        '''

    htmlText = htmlText.format("Resources/iiitk.png", month.upper(), year,
                               id, name, designation, originalPay, originalPayGrade, DOJ, pan,
                               presentPay, incomeTax,
                               da, professionTax,
                               hra,
                               ta,
                               totalEarnings, totalDeductions, netPay)

    printer = QtGui.QPrinter()
    printer.setPageSize(QtGui.QPrinter.A4)
    # printer.setPageMargins(0.5, 1, 0.5, 1, QtGui.QPrinter.Inch)
    paint = printer.paintEngine()
    paint.drawLines(QtCore.QLine(50,50,100,100), 1)
    # printerDialog = QtGui.QPrintDialog(printer)

    document = QtGui.QTextDocument()

    # self.document.setPageSize(QtCore.QSizeF(self.printer.pageRect().size()))
    document.setPageSize(QtCore.QSizeF(printer.paperSize(QtGui.QPrinter.Point)))
    document.setDocumentMargin(28)
    document.setHtml(htmlText)


    dialog = QtGui.QPrintPreviewDialog()
    screen = QtGui.QDesktopWidget().screenGeometry()
    dialog.setGeometry(50, 50, screen.width()-100, screen.height()-100)
    dialog.paintRequested.connect(document.print_)
    dialog.exec_()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    printPaySlip("RANDOM001", "John Doe", "Nobody", 80000, 10000, "24/03/19", "ABCPD1234E",
                120.0, 100, 10, 20, 30, 90000, 100000, 80000, 20000,"February",2019)
    sys.exit()