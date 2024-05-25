from entities.models import BaseModel
from peewee import *

class Discount(BaseModel):
    id = AutoField(primary_key=True, null=True, column_name='Id')
    description = CharField(column_name='Description', null=True)
    percent = FloatField(column_name='Percent')
    end_date = DateField(column_name='EndDate', formats=["%Y/%m/%d"])
    quantity = IntegerField(column_name='Quantity')
    start_date = DateField(column_name='StartDate')
    created_date = DateTimeField(column_name='CreatedDate')
    updated_date = DateTimeField(column_name='UpdateDate', null=False)

    class Meta:
        db_table = "Discount"