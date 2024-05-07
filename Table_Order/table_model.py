import mysql.connector
from peewee import *
from datetime import date, datetime
from database.abc_common_db import abcCommonDb
from database.connection import Connection
class TableModellSQL(Model):
    id = PrimaryKeyField()
    tableNum = IntegerField()
    seatNum = IntegerField()
    status = IntegerField()
    createdDate = DateTimeField()
    updatedDate = DateTimeField()
class TableModel:
    def __init__(self, id, table_num, seat_num, status):
        self.__id = id
        self.__table_num = table_num
        self.__seat_num = seat_num
        self.__status = status
        self.__createdDate = datetime.now()
        self.__updatedDate = None

    @property
    def id(self):
        return self.__id

    @property
    def table_num(self):
        return self.__table_num