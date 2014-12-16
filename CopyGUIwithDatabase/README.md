fileCopyGUIwithDB
=================

Add SQLITE3 database onto file copy utility to store last run time of utility.  Instead of searching last 24 hours for created/modified text files, it now searches since last run time.

Run the GUI fileCopyUtilityUI.py, which utilizes the modules fileCopyUtility.py and fileCopyUtilityDBConnection.py for running the copy function and connecting to the database, respectively.

===

Prompt:

Title: Database functionality for File Transfer - Python 2.7 - IDLE

Scenario: You recently created a script that will check a folder for new or modified files, and then copy those new or modified files to another location. You also created a UI that makes using the script easier and more versatile.

Users are reporting issues with the current system you've made.  Specifically, they are having to manually initiate the 'file check' script at the same time each day. Because they aren't doing this at the EXACT same time each day, some files that were edited right around the time the script was meant to be run were missed, and weren't copied to the outgoing files destination.
 
This means you will have to provide for recording the last time the 'file check' process was performed, so that you can be sure to cover the entire time period in which new or edited files could occur. 

To do this, you will need to create a database with a table that can store the date and time of the last 'file check' process. That way, you can use that date/time as a reference point in terms of finding new or modified files.
 
As part of this project, the users are asking that their UI display the date and time of the last 'file check' process. 

You have been asked to implement this functionality. This means that you will need to: 
- create a database and a table 
- modify your script to both record date/time of 'file check' runs and to retrieve that data for use in the 'file check' process, and 
- modify the UI to display the last 'file check' date/time 

Guidelines: 
Use Python 2.7 for this drill. 
Use sqlite for your database functionality. 
Use wxPython to modify the UI. 
The layout of the UI is up to you. 


