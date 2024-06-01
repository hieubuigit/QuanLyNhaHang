
from peewee import *
from share.base_model import BaseModel
from share.common_config import TableType


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


