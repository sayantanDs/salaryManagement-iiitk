import mysql.connector
import mysql.connector.locales.eng.client_error # imported for proper compilation with PyInstaller
# for more info: https://stackoverflow.com/questions/23657934/mysql-connector-bug-during-except-when-compiled-with-pyinstaller
import hashlib
from CustomClasses import Employee, Designation, Salary
from PySide import QtGui, QtCore
from CustomWidgets import ReconnectMsg

class Database:
    """A class that keeps an instance of DatabaseManager class in a static variable

    A DatabaseManager object connects to MySQL server during creation. Making a new instance of
    DatabaseManager class everytime a database operation is to be done would mean creating new
    connections everytime. This would be slow and redundant. Hence keeping one instance that
    can be used everywhere is better.

    This class stores an instance of DatabaseManager class in a static variable which can be accessed
    using static method Database.getdb(). The connection needs to be created before using getdb for
    the first time using Database.connect() method.

    Example::

        Database.connect(host="localhost",
                        databaseName="test_db",
                        username="root",
                        password="root")

        Database.getdb().addEmployee(emp)   # emp is an Employee object

    """

    __instance = None   # static variable where instance of DatabaseManager is stores

    @staticmethod
    def connect(host, databaseName, username, password=None):
        """Creates connection to server

        Attempts to connect to given host and database using username and password(if any)

        Args:
            host: host name or ip address
            databaseName: MySQL database name
            username: username to be used
            password: password to be used (if any)
                (default is None)

        Returns:
            None

        """
        Database.__instance = DatabaseManager(host,
                                              databaseName,
                                              username,
                                              password)
    @staticmethod
    def getdb():
        """Returns an instance of DatabaseManager class

        This method first ensures that a connection to server exists. If Database was never connected
        using the connect() method, an Exception is raised. If connection was previously made, it pings the
        server to make sure it is still connected. If ping fails, it attempts to reconnect to server. On failure
        of ping and reconnection, mysql.connector.Error is raised.

        If all steps above goes fine without any problems, the instance of DatabaseManager is returned

        Returns:
            DatabaseManager: The instance of DatabaseManager stored is returned

        """
        if Database.__instance is None:
            raise Exception("Database needs to be connected first using connect()!")
        try:
            Database.__instance.reconnect()
        except mysql.connector.Error as e:
            raise e
        return Database.__instance


class Thread(QtCore.QThread):
    """Modified QThread to accept a function and run in a separate thread

    The constructor accepts a function which is to be run in a separate thread.
    The function is run inside a try except block, which excepts mysql.connector.Error as this Thread class
    was made only for running mysql ping function in a separate thread.

    Thread contains a 'success' flag which is initially set to True. If an exception occurs during run(),
    success is set to False. The isSuccess() method can be used to get the success status.

    """
    def __init__(self, func):
        """
        Args:
            func: The function to be run in a separate thread
        """

        QtCore.QThread.__init__(self)
        self.__func = func
        self.__success = True

    def run(self):
        """Starts execution of the function in a separate thread"""

        try:
            self.__func()
        except mysql.connector.Error:
            self.__success = False

    def isSuccess(self):
        """

        Returns:
            bool: The success status

        """
        return self.__success


class DatabaseManager:
    """Class to manage all database access

    This class wraps up MySQL commands in python functions so these function can be easily used without worrying
    about the actual MySQL commands.

    Example:
        To add an employee simply write::

            db.addEmployee(emp)   # assuming db is an instance of DatabaseManager

    """

    def __init__(self, host, databaseName, username, password=None):
        """The constructor conects to the MySQL database using given parameters

        Args:
            host: host name or ip address
            databaseName: MySQL database name
            username: username to be used
            password: password to be used (if any)
                (default is None)
        """

        self.mydb = mysql.connector.connect(
            host=host,
            user=username,
            passwd=password,
            database=databaseName,
            connection_timeout=5
        )

        self.designationTableName = "designations"
        self.employeeTableName = "employees"
        self.loginTablename = "login"
        self.salaryTableName = "salary"

        self.mycursor = self.mydb.cursor()

        self.__msg = ReconnectMsg()     # message to be shown on server reconnection attempt

    def reconnect(self):
        """Function to ping the server and reconnect if connection is lost

        This method starts to ping the server in a different thread using the Thread class. If the ping is not
        finished in a few milliseconds, it would probably mean connection was lost and it is trying to reconnect.
        In this case a reconnect message is shown using ReconnectMsg class. After successful reconnction, the
        method ends. If reconnection fails, a mysql.connector.Error is raised

        Returns:
            None

        """

        t = Thread(lambda: self.mydb.ping(reconnect=True, attempts=1, delay=0))
        t.start()
        i = 0
        while t.isRunning() and i < 1000:
            QtCore.QThread.msleep(5)
            i += 5
        if t.isRunning():
            self.__msg.show()
            QtCore.QCoreApplication.processEvents()
            t.wait()

        self.__msg.hide()

        if not t.isSuccess():
            raise mysql.connector.Error(errno=2003, msg="Can't connect to MySQL server")

    def checkLogin(self, username, password):
        """To check if given username password is correct

        Used for admin login.

        Args:
            username (str): admin username
            password (str): admin password

        Returns:
            bool: True if correct, False otherwise
        """

        self.mycursor.execute("SELECT password FROM " + self.loginTablename + " WHERE username = %s", (username,))
        pswd = self.mycursor.fetchone()
        if pswd is not None and hashlib.sha256(password).digest() == pswd[0]:
            return True
        return False

    def addLogin(self, username, password):
        """To register a new admin username password

        Args:
            username (str): admin username
            password (str): admin password

        Returns:
            None
        """

        hashpass = hashlib.sha256(password).digest()
        self.mycursor.execute("INSERT INTO " + self.loginTablename + " VALUES(%s, %s)", (username, hashpass))
        self.mydb.commit()

    def addEmployee(self, emp):
        """Add a new employee record to database

        Args:
            emp (Employee): Employee object representing the new employee

        Returns:
            None

        """

        insert = "INSERT INTO " + self.employeeTableName + " VALUES(%s, %s, %s, %s, %s, %s, %s)"
        self.mycursor.execute(insert, tuple(emp))
        self.mydb.commit()

    def delEmployee(self, id):
        """Delete existing employee record from database

        Args:
            id (str): ID of the employee to be deleted

        Returns:
            None
        """

        command = "DELETE FROM " + self.employeeTableName + " WHERE ID = %s"
        self.mycursor.execute(command, (id,))
        self.mydb.commit()

    def editEmployee(self, emp):
        """Edit employee details of an existing employee record

        Args:
            emp (Employee): Employee object with updated employee details

        Returns:
            None
        """

        command = "UPDATE " + self.employeeTableName + " " + \
                  "SET name = %s, " + \
                  "Designation = %s, " + \
                  "OriginalPay = %s, " + \
                  "OriginalGradePay = %s, " + \
                  "DOJ = %s, " + \
                  "Pan = %s " + \
                  "WHERE ID = %s"

        t = tuple(list(emp)[1:] + [emp.id])     # rearrange info according to order needed for database
        self.mycursor.execute(command, t)
        self.mydb.commit()

    # def changeDetail(self, id, field, newText):
    #     print "id=", id
    #     print "field=", field
    #     command = "update " + self.employeeTableName + " set " + field + " = %s where ID = %s"
    #     print "command=", command
    #     self.mycursor.execute(command, (newText, id))
    #     self.mydb.commit()

    def getEmployeeNameList(self):
        """Get list of unique names of all employees in database

        Returns:
            list of str: A list of all unique employee names in database

        """

        self.mycursor.execute("SELECT DISTINCT name FROM " + self.employeeTableName)
        list = [str(x[0]) for x in self.mycursor.fetchall()]
        list.sort()
        return list

    def getIdListForName(self, name):
        """Get a list of IDs of all employees having the given name.

        This method returns IDs of all employees having the given name (may return only one ID if only one such
        employee exists)

        Args:
            name (str): Name of employee(s) who's ID(s) are required

        Returns:
            list of str: A list of IDs of all employees having the given name

        """
        command = "SELECT ID FROM " + self.employeeTableName + " WHERE name = %s"
        self.mycursor.execute(command,(name,))
        list = [str(x[0]) for x in self.mycursor.fetchall()]
        return list

    def getEmployeeInfo(self, id):
        """Get all details about the employee with given ID stored in the database

        Args:
            id (str): ID for which employee details are required

        Returns:
            Employee: An Employee object with required details
        """
        command = "SELECT * FROM " + self.employeeTableName + " WHERE ID = %s"
        self.mycursor.execute(command,(id,))
        res = self.mycursor.fetchone()
        if res is None:
            return None
        return Employee(*res)

    def getAllEmployeeInfo(self):
        """Get list of all employee details

        Returns:
            list: details of all employees
        """
        command = "SELECT * FROM " + self.employeeTableName
        self.mycursor.execute(command)
        return self.mycursor.fetchall()

    def getAllDesignationInfo(self):
        """Get list of all designation details

        Returns:
            list: details of all designations
        """
        command = "SELECT * FROM " + self.designationTableName
        self.mycursor.execute(command)
        return self.mycursor.fetchall()


    def getDesignations(self):
        """Get a list of all the designation names stored in database

        Returns:
            list of str: list of all designation names in the database
        """
        self.mycursor.execute("SELECT designation FROM %s"%self.designationTableName)
        list = [str(x[0]) for x in self.mycursor.fetchall()]
        return list

    # def addDesignation(self, designation, da, ha, ta, it, pt):
    def addDesignation(self, desig):
        """Add a new designation to the database

        Args:
            desig (Designation): Designation object representing designation to be added in database

        Returns:
            None

        """
        insert = "INSERT INTO " + self.designationTableName + "  VALUES(%s, %s, %s, %s, %s, %s)"
        self.mycursor.execute(insert, desig.toTuple())
        self.mydb.commit()

    def getDesignationInfo(self, designation):
        """Get designation info for given designation name

        Args:
            designation (str): Name of the designation who's information is required

        Returns:
            Designation: Designation object representing designation with given name

        """
        command = "SELECT * FROM " + self.designationTableName + " WHERE designation = %s"
        self.mycursor.execute(command,(designation,))
        res = self.mycursor.fetchone()
        if res is None:
            return None
        return Designation(*res)

    def editDesignationInfo(self, desig, origDesignation):
        """Edit designation details of existing designation in database

        Args:
            desig (Designation): Designation object with updated designation info
            origDesignation: current designation name

        Returns:
            None

        """
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
        """Save record of calculated salary

        Args:
            salary (Salary): Salary object representing calculated salary

        Returns:
            None

        """
        insert = "INSERT INTO " + self.salaryTableName + "  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.mycursor.execute(insert, salary.toTuple())
        self.mydb.commit()

    def replaceSalary(self, salary):
        """Replace a record of previously calculated salary

        This may be used if there was a mistake during calculation last time.

        Args:
            salary (Salary): Salary object representing calculated salary

        Returns:
            None

        """
        delete = "DELETE FROM " + self.salaryTableName + "  WHERE ID=%s AND Date=%s"
        self.mycursor.execute(delete, (salary.id, salary.date))
        self.saveSalary(salary)

    def getSalary(self, id, month, year):
        """Get salary record for for given month and year saved for employee with given ID

        Args:
            id (str): ID of the employee
            month (str): month of salary
            year (int): year of salary

        Returns:
            Salary: salary object representing the calculated salary for the employee for that month and year

        """
        command = "SELECT * FROM " + self.salaryTableName + "  WHERE ID=%s AND Date=%s"
        date = Salary.monthYearToDate(month, year)
        self.mycursor.execute(command, (id, date))
        res = self.mycursor.fetchone()
        id = res[0]
        emp = self.getEmployeeInfo(id)

        t = (emp,) + res[1:]
        return Salary(*t)
