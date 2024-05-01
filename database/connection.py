import mysql.connector
from mysql.connector import errorcode
from peewee import *


class Connection:
    CONFIG = {
        'user': "root",
        'database': "quanlynhahang",
        'password': "123456789",
        'host': "localhost",
    }

    def __init__(self):
        db = MySQLDatabase(self.CONFIG['database'])
        db.connect()
        self.__connection = None
        self.__cursor = None

    @property
    def cursor(self):
        return self.__cursor

    @cursor.setter
    def cursor(self, cursor):
        self.__cursor = cursor

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
        else:
            self.__connection.close()

    def close(self):
        self.__connection.close()
        self.__cursor.close()
