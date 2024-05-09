import mysql.connector
from peewee import *
from datetime import date, datetime
from database.abc_common_db import abcCommonDb
from database.connection import Connection

dbhandle = MySQLDatabase(
    database="QuanLyNhaHang", user="root",
    password="123456789",
    host='localhost'
)
class BaseModel(Model):
    class Meta:
        database = dbhandle
class Table(BaseModel):
    id = AutoField(primary_key=True, null=True)
    tableNum = IntegerField()
    seatNum = IntegerField()
    status = IntegerField()
    createdDate = DateTimeField(datetime.now())
    updatedDate = DateTimeField()
    class Meta:
        db_name = "Table"


