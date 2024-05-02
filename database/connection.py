import mysql.connector
from mysql.connector import errorcode


class Connection:
    CONFIG = {
        'user': "root",
        'database': "quanlynhahang",
        'password': "123456789",
        'host': "localhost",
    }

    def __init__(self):
        self.__connection = None
        self.__cursor = None
        self.connect()

    @property
    def cursor(self):
        return self.__cursor

    def connect(self):
        try:
            self.__connection = mysql.connector.connect(**Connection.CONFIG)
            self.__cursor = self.__connection.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close(self):
        self.__connection.close()
        self.__cursor.close()
