import mysql.connector
from peewee import *
from datetime import date, datetime

from share.base_model import BaseModel


class Table(BaseModel):
    id = AutoField(primary_key=True, null=False)
    tableNum = IntegerField()
    seatNum = IntegerField()
    status = IntegerField()
    createdDate = DateTimeField(datetime.now())
    updatedDate = DateTimeField()
    class Meta:
        db_table = "Table"


