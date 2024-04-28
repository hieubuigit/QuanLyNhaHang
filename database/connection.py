import mysql.connector
from mysql.connector import errorcode

class Connection:
    CONFIG = {
        'user': "root",
        'database': "quanlybanhang",
        'password': "123456789",
        'host': "localhost",
    }

    def  __init__(self):
        pass

    def connect(self):
        try:
            cnx = mysql.connector.connect(**Connection.CONFIG)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()

    def close(self):
        pass