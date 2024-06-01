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
    totalMoney = DecimalField(null=False, column_name="TotalMoney", max_digits=15, decimal_places=3)
    type = IntegerField(null=False, column_name="Type")
    createdDate = DateTimeField(column_name="CreateDate", formats=["%Y-%m-%d"])
    updatedDate = DateTimeField(column_name="UpdateDate", null=True, formats=["%Y-%m-%d"])
    class Meta:
        db_table = "Billing"

    def __str__(self):
        return str([id, self.tableId, self.userId, self.creatorName, self.customerName, self.totalMoney, self.type])
