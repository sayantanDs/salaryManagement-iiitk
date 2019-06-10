import mysql.connector
import hashlib
from CustomClasses import Employee, Designation

class Database:
    __instance = None

    @staticmethod
    def connect(host, databaseName, username, password=None):
        Database.__instance = DatabaseManager(host,
                                              databaseName,
                                              username,
                                              password)
    @staticmethod
    def getdb():
        if Database.__instance is None:
            raise Exception("Database connection needs to be created first using creatdb()!")
        try:
            Database.__instance.mydb.ping(reconnect=True, attempts=1, delay=0)
        except mysql.connector.Error as e:
            raise e
        return Database.__instance

'''
Class to manage all database access
'''
class DatabaseManager:
    def __init__(self, host, databaseName, username, password=None):

        self.mydb = mysql.connector.connect(
            host=host,
            user=username,
            passwd=password,
            database=databaseName
        )

        self.designationTableName = "designations"
        self.employeeTableName = "employees"
        self.loginTablename = "login"
        self.salaryTableName = "salary"

        self.mycursor = self.mydb.cursor()

    def checkLogin(self, username, password):
        # if username == "admin" and password == "1234":
        #     return True
        # return False
        self.mycursor.execute("SELECT password FROM " + self.loginTablename + " WHERE username = %s", (username,))
        pswd = self.mycursor.fetchone()
        if pswd is not None and hashlib.sha256(password).digest() == pswd[0]:
            return True
        return False

    def addLogin(self, username, password):
        hashpass = hashlib.sha256(password).digest()
        self.mycursor.execute("INSERT INTO " + self.loginTablename + " VALUES(%s, %s)", (username, hashpass))
        self.mydb.commit()

    def addEmployee(self, emp):
        insert = "INSERT INTO " + self.employeeTableName + " VALUES(%s, %s, %s, %s, %s, %s, %s)"
        self.mycursor.execute(insert, tuple(emp))
        self.mydb.commit()

    # Edited by Sattam
    def delEmployee(self, id):
        command = "DELETE FROM " + self.employeeTableName + " WHERE ID = %s"
        self.mycursor.execute(command, (id,))
        self.mydb.commit()

    def editEmployee(self, emp):
        command = "UPDATE " + self.employeeTableName + " " + \
                  "SET name = %s, " + \
                  "Designation = %s, " + \
                  "OriginalPay = %s, " + \
                  "OriginalGradePay = %s, " + \
                  "DOJ = %s, " + \
                  "Pan = %s " + \
                  "WHERE ID = %s"
        print command
        t = tuple(list(emp)[1:] + [emp.id])
        self.mycursor.execute(command, t)
        self.mydb.commit()

    def changeDetail(self, id, field, newText):
        print "id=", id
        print "field=", field
        command = "update " + self.employeeTableName + " set " + field + " = %s where ID = %s"
        print "command=", command
        self.mycursor.execute(command, (newText, id))
        self.mydb.commit()

    def getEmployeeNameList(self):
        self.mycursor.execute("SELECT DISTINCT name FROM " + self.employeeTableName)
        list = [str(x[0]) for x in self.mycursor.fetchall()]
        list.sort()
        return list

    def getIdListForName(self, name):
        command = "SELECT ID FROM " + self.employeeTableName + " WHERE name = %s"
        self.mycursor.execute(command,(name,))
        list = [str(x[0]) for x in self.mycursor.fetchall()]
        return list

    def getEmployeeInfo(self, id):
        command = "SELECT * FROM " + self.employeeTableName + " WHERE ID = %s"
        self.mycursor.execute(command,(id,))
        res = self.mycursor.fetchone()
        if res is None:
            return None
        return Employee(*res)

    def getAllEmployeeInfo(self):
        command = "SELECT * FROM " + self.employeeTableName
        self.mycursor.execute(command)
        return self.mycursor.fetchall()

    def getAllDesignationInfo(self):
        command = "SELECT * FROM " + self.designationTableName
        self.mycursor.execute(command)
        return self.mycursor.fetchall()


    def getDesignations(self):
        self.mycursor.execute("SELECT designation FROM %s"%self.designationTableName)
        list = [str(x[0]) for x in self.mycursor.fetchall()]
        return list

    # def addDesignation(self, designation, da, ha, ta, it, pt):
    def addDesignation(self, desig):
        insert = "INSERT INTO " + self.designationTableName + "  VALUES(%s, %s, %s, %s, %s, %s)"
        self.mycursor.execute(insert, desig.toTuple())
        self.mydb.commit()

    def getDesignationInfo(self, designation):
        command = "SELECT * FROM " + self.designationTableName + " WHERE designation = %s"
        self.mycursor.execute(command,(designation,))
        res = self.mycursor.fetchone()
        if res is None:
            return None
        return Designation(*res)

    def editDesignationInfo(self, desig, origDesignation):
        command="update " + self.designationTableName+" " +\
                "set designation = %s ,"+\
                "DA = %s, "+\
                "HA = %s, "+\
                "TA = %s, "+\
                "IT = %s, "+\
                "PT = %s "+\
                "where designation = %s"
        self.mycursor.execute(command, tuple(desig) + (origDesignation,))
        if desig.designation != origDesignation:
            command = "update " + self.employeeTableName + " set designation=%s where designation=%s"
            print command
            self.mycursor.execute(command, (desig.designation, origDesignation))
        self.mydb.commit()

    def saveSalary(self, salary):
        insert = "INSERT INTO " + self.salaryTableName + "  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.mycursor.execute(insert, salary.toTuple())
        self.mydb.commit()

    def replaceSalary(self, salary):
        delete = "DELETE FROM " + self.salaryTableName + "  WHERE ID=%s AND Date=%s"
        self.mycursor.execute(delete, (salary.id, salary.date))
        self.saveSalary(salary)
