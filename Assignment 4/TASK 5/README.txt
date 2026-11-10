TASK 5 - Attendance Utility in Four Organisations
=================================================

Folder contents:
1. Organisation_A_Single_Script
   Run: python attendance_single.py

2. Organisation_B_Module_and_Main
   Run from this folder: python main.py

3. Organisation_C_Three_Modules
   Run from this folder: python main.py

4. Organisation_D_Package
   Run from this folder: python main.py

Expected output for A and B:
Attendance: 80.00%
Longest consecutive absence: 2

Expected output for C and D:
Valid records: 6
Attendance percentage: 50.00%
Longest consecutive absence: 2
Rejected rows: 2
(7, 'invalid date')
(8, 'status must be P or A')

The same attendance calculations are used in all four structures.
For C and D, attendance.csv includes two intentionally invalid rows
to demonstrate validation and rejected-row reporting.
