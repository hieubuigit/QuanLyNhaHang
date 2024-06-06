from datetime import datetime

from peewee import Model, InternalError
from entities.models import database, Billing, User, OrderList, Table
from share.common_config import UserType, StatusTable
from share.utils import Utils


class BillModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with database:
            database.create_tables([Billing, OrderList, Table], safe=True)

    def get_bills_by_user_type(self, user_type):
        try:
            if user_type == UserType.ADMIN.value:
                results = Billing.select().order_by(Billing.createdDate.desc())
                if results:
                    return results
            else:
                results = Billing.select(Billing, User).join(User).where(Billing.userId == Utils.user_profile["id"])
                if results:
                    return results
        except InternalError as px:
            print(str(px))

    def get_bill_by_date(self, by_date):
        try:
            results = Billing.select().where(Billing.createdDate.year == by_date.year
                                             and Billing.createdDate.month == by_date.month
                                             and Billing.createdDate.day == by_date.day)

            if results:
                return results
        except InternalError as px:
            print(str(px))

    def save_bill(self, user_id, customer_name, customer_phone, money, bill_type, created_date, status_bill):
        try:
            row = Billing(userId=user_id,
                          customerName=customer_name,
                          customerPhoneNumber=customer_phone,
                          totalMoney=money,
                          type=bill_type,
                          status=status_bill,
                          createdDate=created_date)

            bill = row
            bill.save()
        except InternalError as px:
            print(str(px))

    def delete_bill(self, bill_id):
        try:
            b = Billing.get_or_none(Billing.id == bill_id)
            if b:
                OrderList.delete().where(OrderList.billing_id == b.id)
                if b.tableId:
                    t = Table.get_or_none(Table.id == b.tableId)
                    if t:
                        table = t
                        table.status = StatusTable.AVAILABLE.value[0]
                        table.save()
                b.delete_instance()
        except InternalError as px:
            print(str(px))

    def update_bill(self, id, create_date, customer_name, customer_phone, money, bill_type, status_bill):
        try:
            b: Billing = Billing.get(Billing.id == id)
            b.customerName = customer_name
            b.customerPhoneNumber = customer_phone
            b.money = money
            b.type = bill_type
            b.createdDate = create_date
            b.status = status_bill
            b.updatedDate = datetime.now()
            b.save()
        except InternalError as px:
            print(str(px))

    def get_user_name(self, _id):
        try:
            u = User.table_exists()
            if not u:
                User.create_table()
            user: User = User.get_or_none(User.id == _id)
            if user:
                return user.user_name
        except InternalError as px:
            print(str(px))

    def get_table_num(selfs, _id):
        try:
            t = Table.table_exists()
            if not t:
                Table.create_table()
            t: Table = Table.get_or_none(Table.id == _id)
            if t:
                return t.tableNum
        except InternalError as px:
            print(str(px))
