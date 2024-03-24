import mysql.connector
from mysql.connector import errorcode

config = {
    'user': "root",
    'database': "quanlybanhang",
    'password': "123456789",
    'host': "localhost",
}

try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()