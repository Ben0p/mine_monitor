
import mysql.connector

mydb = mysql.connector.connect(
  host="solopstetra01.fmgops.local",
  user="root",
  passwd="tetra",
  database="tetraflexlogdb"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT Timestamp, NodeNo, Description, RadioRegMsCount FROM `nodestatus` WHERE StdBy = '0';")

myresult = mycursor.fetchall()

node_status = [
  {
    'timestamp' : x[0],
    'node_number' : x[1],
    'node_description' : x[2],
    'radio_count' : x[3]
  } for x in myresult]

print(node_status)