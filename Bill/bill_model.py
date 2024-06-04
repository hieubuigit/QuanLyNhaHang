from peewee import *
from entities.models import User


class BillModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_bills_by_date(self, by_date):
        pass
        # b = Billing.table_exists()
        # if not b:
        #     Billing.create_table()
        # results = Billing.select().where(Billing.createdDate.year == by_date.year
        #                                  and Billing.createdDate.month == by_date.month
        #                                  and Billing.createdDate.day == by_date.day)
        # return results

    def save_bill(self, bill):
        pass
        # b = Billing.table_exists()
        # if not b:
        #     Billing.create_table()
        # bill = bill
        # bill.save()

    def delete_by_id(self, id):
        pass
        # product = Billing.get_or_none(Billing.id == id)
        # if product:
        #     product.delete_instance()
        #     return True
        return False

    def update_by_id(self, id, creator_name, create_date, customer_name, customer_phone, money, bill_type):
        # b = Billing.get(Billing.id == id)
        # b.creatorName = creator_name
        # b.customerName = customer_name
        # b.customerPhoneNumber = customer_phone
        # b.money = money
        # b.type = bill_type
        # b.createdDate = create_date
        # b.updatedDate = datetime.now()
        # b.save()
        pass

    def get_user_by_id(self, _id):
        u = User.table_exists()
        if not u:
            User.create_table()
        row = User.select().where(User.id == _id)
        return row
    def get_discount(self):
        d = Discount.table_exists()
        if not d:
            Discount.create_table()
        results = Discount.select()
        return results