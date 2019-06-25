.. Salary Management IIIT Kalyani documentation master file, created by
   sphinx-quickstart on Sat Jun 22 18:41:20 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Salary Management System's documentation!
==========================================================

This documentation is for the application made to serve as Salary Management System for
**Indian Institute of Information Technology Kalyani**.
This application is made and maintained by the students of this institute.

Overview
---------

This application needs to calculate salary for every employee and generate a payslip.
So record of every employee needs to stored in a database. All employees in
a certain designation have same allowances and deductions. Thus, instead of storing
allowances and deductions for everyone individually, we may store a list of designations
and their corresponding allowances and deductions. The database contains a
*designation table* and an *employee table*. We lookup the designation of an employee from the
*employee table* and corresponding allowances and deductions from *designation table*.
The GUI contains pages for adding, editing, deleting and showing all employee records.
Similary it also has pages for adding, editing, deleting and showing all designation records.

Some important modules
^^^^^^^^^^^^^^^^^^^^^^^^^

- The :py:mod:`CustomClasses` module has the following classes

   - The employees are represented with :py:mod:`Employee <CustomClasses.Employee.Employee>` class,
   - Designation using :py:mod:`Designation <CustomClasses.Designation.Designation>` class and
   - Salary with :py:mod:`Salary <CustomClasses.Salary.Salary>` class.

- The :py:mod:`DatabaseManager <DatabaseManager.databaseManager>` module handles all database transactions.

- The :py:mod:`CustomWidgets` module has widgets specially made for this application

- The application starts from the :py:mod:`main` module

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   CustomClasses
   CustomWidgets
   DatabaseManager

   main
   Header
   Home
   Login

   AddEmployee
   EditEmployee
   DelEmployee
   ShowEmployee

   AddDesignation
   EditDesignation
   ShowDesignation

   CalculateSalary
   ShowPaySlip
   printPaySlip

   ShowMySqlError


