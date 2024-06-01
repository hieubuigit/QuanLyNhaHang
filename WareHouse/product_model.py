from enum import Enum

import peewee

from database.connection import Connection
from share.base_model import BaseModel
from peewee import *

class ProductType(Enum):
    Food = 0
    Drink = 1
class Product(BaseModel):
    id = AutoField(primary_key=True, null=True)
    name = CharField(null=True)
    price = DecimalField()
    unit = CharField()
    quantity = IntegerField()
    capacity = FloatField(null=False)
    alcohol = FloatField(null=False)
    productType = IntegerField()
    image = BlobField()
    createdDate = DateTimeField()
    updatedDate = DateTimeField(null=False)

    def __str__(self):
        return str([id, self.name, self.price, self.unit, self.quantity, self.capacity,
                    self.alcohol, self.productType, self.image])

    class Meta:
        db_table = "Product"
