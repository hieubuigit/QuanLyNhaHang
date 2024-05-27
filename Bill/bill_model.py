from peewee import *
from WareHouse.discount_model import Discount
from entities.models import User
from share.base_model import BaseModel
from Table_Order.table_model import Table

class Billing(BaseModel):
    id = AutoField(primary_key=True, null=False)
    tableId = ForeignKeyField(null=True, column_name="TableId", field='id', model=Table)
    userId = ForeignKeyField(null=True, column_name="UserId",  field='id', model=User)
    creatorName = CharField(null=True, column_name="CreatorName")
    discountId = ForeignKeyField(null=True, column_name="DiscountId", field='id', model=Discount)
    customerName = CharField(null=True, column_name="CustomerName")
    customerPhoneNumber = CharField(null=True, column_name="CustomerPhone")
    totalMoney = DecimalField(null=False, column_name="TotalMoney")
    type = IntegerField(null=False)
    createdDate = DateTimeField(formats=["%Y-%m-%d"])
    updatedDate = DateTimeField(null=True)
    class Meta:
        db_table = "Billing"
