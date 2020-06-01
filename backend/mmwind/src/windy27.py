import pyodbc
import json
import datetime
import time



# driver = "{ODBC Driver 17 for SQL Server}"
driver = 'FreeTDS'
server = 'SOLOPSRS02' 
username = 'FMG\\svc.sol.wind' 
password = '5U!Y7$gaxS!NVnO78l$c' 

cnxn = pyodbc.connect('DRIVER=FreeTDS;SERVER=SOLOPSRS02;UID=FMG\\svc.sol.wind;PWD=5U!Y7$gaxS!NVnO78l$c;')

cursor = cnxn.cursor()