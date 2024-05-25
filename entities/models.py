from peewee import *

database = MySQLDatabase('quanlynhahang', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'user': 'root', 'password': '123456789'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Billing(BaseModel):
    created_date = DateTimeField(column_name='CreatedDate', null=True)
    customer_name = CharField(column_name='CustomerName')
    customer_phone_number = CharField(column_name='CustomerPhoneNumber')
    discount_id = IntegerField(column_name='DiscountId')
    id = AutoField(column_name='Id')
    table_id = IntegerField(column_name='TableId')
    total_money = DecimalField(column_name='TotalMoney')
    updated_date = DateTimeField(column_name='UpdatedDate', null=True)
    user_id = IntegerField(column_name='UserId')

    class Meta:
        table_name = 'billing'

class Discount(BaseModel):
    created_date = DateTimeField(column_name='CreatedDate')
    description = CharField(column_name='Description', null=True)
    end_date = DateField(column_name='EndDate')
    id = AutoField(column_name='Id')
    percent = FloatField(column_name='Percent')
    quantity = IntegerField(column_name='Quantity')
    start_date = DateField(column_name='StartDate')
    updated_date = DateTimeField(column_name='UpdatedDate', null=True)

    class Meta:
        table_name = 'discount'

class Product(BaseModel):
    alcohol = FloatField(column_name='Alcohol')
    capacity = FloatField(column_name='Capacity')
    created_date = DateTimeField(column_name='CreatedDate')
    id = AutoField(column_name='Id')
    image = CharField(column_name='Image')
    name = CharField(column_name='Name')
    price = DecimalField(column_name='Price')
    product_type = IntegerField(column_name='ProductType')
    quantity = FloatField(column_name='Quantity')
    unit = IntegerField(column_name='Unit')
    updated_date = DateTimeField(column_name='UpdatedDate', null=True)

    class Meta:
        table_name = 'product'

class Orderlist(BaseModel):
    billing = ForeignKeyField(column_name='BillingId', field='id', model=Billing)
    created_date = DateTimeField(column_name='CreatedDate', null=True)
    cur_price = DecimalField(column_name='CurPrice')
    id = AutoField(column_name='Id')
    product = ForeignKeyField(column_name='ProductId', field='id', model=Product)
    quantity = IntegerField(column_name='Quantity')
    updated_date = DateTimeField(column_name='UpdatedDate', null=True)

    class Meta:
        table_name = 'orderlist'

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

class Payslip(BaseModel):
    created_date = DateTimeField(column_name='CreatedDate', null=True)
    hours = FloatField(column_name='Hours', null=True)
    id = AutoField(column_name='Id')
    total_salary = DecimalField(column_name='TotalSalary', null=True)
    updated_date = DateTimeField(column_name='UpdatedDate', null=True)
    user = ForeignKeyField(column_name='UserId', field='id', model=User)

    class Meta:
        table_name = 'payslip'

class Table(BaseModel):
    created_date = DateTimeField(column_name='CreatedDate', null=True)
    id = AutoField(column_name='Id')
    seat_num = IntegerField(column_name='SeatNum')
    status = IntegerField(column_name='Status', null=True)
    table_num = IntegerField(column_name='TableNum')
    updated_date = DateTimeField(column_name='UpdatedDate', null=True)

    class Meta:
        table_name = 'table'

class Warehouse(BaseModel):
    created_date = DateTimeField(column_name='CreatedDate', null=True)
    id = AutoField(column_name='Id')
    invoice_code = CharField(column_name='InvoiceCode', null=True)
    total_money = DecimalField(column_name='TotalMoney')
    updated_date = DateTimeField(column_name='UpdatedDate', null=True)
    user = ForeignKeyField(column_name='UserId', field='id', model=User)

    class Meta:
        table_name = 'warehouse'

