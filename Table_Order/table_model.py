from peewee import *
from datetime import date, datetime
from database.abc_common_db import abcCommonDb
from database.connection import Connection
class Table(Model):
    id = PrimaryKeyField()
    tableNum = IntegerField()
    seatNum = IntegerField()
    status = IntegerField()
    createdDate = DateTimeField()
    updatedDate = DateTimeField()
class TableModel:
    def __init__(self, **data):
        self.__id = 0
        self.__table_num = data['tableNum']
        self.__seat_num = data['seatNum']
        self.__status = data['status']
        self.__createdDate = datetime.now()
        self.__updatedDate = datetime.now()
