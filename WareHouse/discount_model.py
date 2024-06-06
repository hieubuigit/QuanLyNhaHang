from datetime import datetime
from peewee import Model, InternalError, fn
from entities.models import Discount, database


class DiscountModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with database:
            database.create_tables([Discount], safe=True)

    def get_discounts(self):
        try:
            pr = Discount.table_exists()
            if not pr:
                Discount.create_table()
            rows = Discount.select()
            return rows
        except InternalError as px:
            print(str(px))

    def save_discount(self, desc, percent, start_date, end_date, quantity):
        try:
            row = Discount(description=desc, percent=percent, start_date=start_date, end_date=end_date,
                           quantity=quantity, created_date=f"{datetime.now():%Y-%m-%d}")
            row.save()
        except InternalError as px:
            print(str(px))

    def delete_discount(self, id):
        try:
            d = Discount.get_or_none(Discount.id == id)
            if d:
                d.delete_instance()
        except InternalError as px:
            print(str(px))

    def update_discount(self, _id, percent, desc, quantity, start_date, end_date):
        try:
            d = Discount.get_or_none(Discount.id == _id)
            if d:
                d.percent = percent
                d.description = desc
                d.quantity = quantity
                d.start_date = start_date
                d.end_date = end_date
                d.update_date = datetime.now()
                d.save()
        except InternalError as px:
            print(str(px))

    def search_discounts(self, key):
        try:
            rows = Discount.select().where(fn.Lower(Discount.description).contains(fn.Lower(key)))
            return rows
        except InternalError as px:
            print(str(px))
