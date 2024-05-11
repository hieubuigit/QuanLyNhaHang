from peewee import *
from datetime import date, datetime

from share.base_model import BaseModel
class Billing(BaseModel):
    id = AutoField(primary_key=True, null=False)
    tableId = IntegerField(null=True)
    userId = IntegerField(null=True)
    discountId = IntegerField(null=True)
    customerName = CharField()
    customerPhoneNumber = CharField()
    totalMoney = DecimalField()
    createdDate = DateTimeField(default=datetime.now(), formats=["%Y-%m-%d"])
    updatedDate = DateTimeField(null=True)
    class Meta:
        db_table = "Billing"
