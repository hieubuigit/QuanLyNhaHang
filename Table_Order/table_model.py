from enum import Enum

import mysql.connector
from peewee import *
import datetime

from share.base_model import BaseModel

class TableType(Enum):
    Add = "ADD"
    Normal = "NORMAL"
class Table(BaseModel):
    id = AutoField(primary_key=True, null=True)
    tableNum = CharField()
    seatNum = IntegerField()
    status = IntegerField()
    createdDate = DateTimeField()
    updatedDate = DateTimeField()
    table_type = TableType.Normal

    def __str__(self):
        return str([id, self.tableNum, self.seatNum, self.status, self.createdDate, self.updatedDate])
    class Meta:
        db_table = "Table"


