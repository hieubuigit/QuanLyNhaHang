from peewee import *
from share.common_config import TableType

database = MySQLDatabase('quanlynhahang',
                         **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'user': 'root',
                            'password': '123456789'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


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


class Product(BaseModel):
    id = AutoField(primary_key=True, null=True, column_name="Id")
    name = CharField(null=True, column_name="Name")
    price = DecimalField(null=False, column_name="Price", max_digits=10, decimal_places=0)
    unit = CharField(column_name="Unit")
    quantity = IntegerField(column_name="Quantity")
    capacity = FloatField(null=False, column_name="Capacity")
    alcohol = FloatField(null=False, column_name="Alcohol")
    productType = IntegerField(column_name="Type")
    image = BlobField(column_name="Image")
    createdDate = DateTimeField(column_name="CreatedDate")
    updatedDate = DateTimeField(null=False, column_name="UpdatedDate")

    class Meta:
        db_table = "Product"


class Paygrade(BaseModel):
    allowance = FloatField(column_name='Allowance', null=True)
    created_date = DateTimeField(column_name='CreatedDate', null=True)
    id = AutoField(column_name='Id')
    pay_per_hours = FloatField(column_name='PayPerHours', null=True)
    type = IntegerField(column_name='Type')
    updated_date = DateTimeField(column_name='UpdatedDate', null=True)

    class Meta:
        table_name = 'paygrade'


class User(BaseModel):
    address = CharField(column_name='Address', null=True)
    birth_date = DateField(column_name='BirthDate')
    created_date = DateTimeField(column_name='CreatedDate')
    email = CharField(column_name='Email', null=True)
    first_name = CharField(column_name='FirstName')
    gender = IntegerField(column_name='Gender')
    id = AutoField(column_name='Id')
    identity = CharField(column_name='Identity')
    income_date = DateField(column_name='IncomeDate')
    last_name = CharField(column_name='LastName')
    password = CharField(column_name='Password')
    phone_number = CharField(column_name='PhoneNumber')
    status = IntegerField(column_name='Status')
    type = IntegerField(column_name='Type')
    updated_date = DateTimeField(column_name='UpdatedDate', null=True)
    user_code = CharField(column_name='UserCode')
    user_name = CharField(column_name='UserName')

    class Meta:
        table_name = 'user'


class Table(BaseModel):
    id = AutoField(column_name='Id', primary_key=True, null=True)
    tableNum = CharField(column_name='TableNum', null=True)
    seatNum = IntegerField(column_name='SeatNum', null=True)
    status = IntegerField(column_name='Status', null=True)
    createdDate = DateTimeField(column_name='CreatedDate')
    updatedDate = DateTimeField(column_name='UpdatedDate', null=False)
    table_type = TableType.Normal

    class Meta:
        table_name = "Table"


class Billing(BaseModel):
    id = AutoField(primary_key=True, null=False)
    tableId = ForeignKeyField(null=True, column_name="TableId", field='id', model=Table)
    userId = ForeignKeyField(null=True, column_name="UserId", field='id', model=User)
    # creatorName = CharField(null=True, column_name="CreatorName")
    discountId = ForeignKeyField(null=True, column_name="DiscountId", field='id', model=Discount)
    customerName = CharField(null=True, column_name="CustomerName")
    customerPhoneNumber = CharField(null=True, column_name="CustomerPhoneNumber")
    totalMoney = DecimalField(null=False, column_name="TotalMoney", max_digits=10, decimal_places=0)
    type = IntegerField(null=False, column_name="Type")
    status = IntegerField(column_name="Status", null=False)
    createdDate = DateTimeField(column_name="CreatedDate", formats=["%Y-%m-%d"])
    updatedDate = DateTimeField(column_name="UpdatedDate", null=True, formats=["%Y-%m-%d"])

    class Meta:
        table_name = "Billing"


class OrderList(BaseModel):
    billing_id = ForeignKeyField(column_name='BillingId', field='id', model=Billing)
    created_date = DateTimeField(column_name='CreatedDate', null=True)
    cur_price = DecimalField(column_name='CurPrice', decimal_places=0, max_digits=10)
    id = AutoField(column_name='Id')
    product_id = ForeignKeyField(column_name='ProductId', field='id', model=Product)
    quantity = IntegerField(column_name='Quantity')
    updated_date = DateTimeField(column_name='UpdatedDate', null=True)

    class Meta:
        table_name = 'OrderList'


class Payslip(BaseModel):
    created_date = DateTimeField(column_name='CreatedDate', null=True)
    hours = FloatField(column_name='Hours', null=True)
    id = AutoField(column_name='Id')
    total_salary = DecimalField(column_name='TotalSalary', null=True)
    updated_date = DateTimeField(column_name='UpdatedDate', null=True)
    user = ForeignKeyField(column_name='UserId', field='id', model=User)

    class Meta:
        table_name = 'payslip'


class Warehouse(BaseModel):
    created_date = DateTimeField(column_name='CreatedDate', null=True)
    id = AutoField(column_name='Id')
    invoice_code = CharField(column_name='InvoiceCode', null=True)
    total_money = DecimalField(column_name='TotalMoney')
    updated_date = DateTimeField(column_name='UpdatedDate', null=True)
    user = ForeignKeyField(column_name='UserId', field='id', model=User)

    class Meta:
        table_name = 'warehouse'
