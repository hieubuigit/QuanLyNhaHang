from datetime import datetime
from tkinter import messagebox

from peewee import fn, InternalError
from warehouse.discount_view import DiscountView
from entities.models import Discount


class DiscountController:
    def __init__(self, root):
        self.__discounts = []
        self.get_data()
        self.view = DiscountView(root=root, controller=self)

    @property
    def discounts(self):
        return self.__discounts

    def get_data(self):
        self.__discounts = []
        try:
            pr = Discount.table_exists()
            if not pr:
                Discount.create_table()
            rows = Discount.select()
            self.__discounts.extend(rows)
        except InternalError as px:
            print(str(px))


    def save_data_to_db(self, desc, percent, start_date, end_date, quantity):
        try:

            row = Discount(description=desc, percent=percent, start_date=start_date, end_date=end_date,
                           quantity=quantity, created_date=f"{datetime.now():%Y-%m-%d}")
            row.save()
        except InternalError as px:
            print(str(px))

    def __delete_product(self, _id):
        try:
            d = Discount.get_or_none(Discount.id == _id)
            if d:
                d.delete_instance()
            else:
                print(f"No record found with ID {_id}")
        except InternalError as px:
            print(str(px))


    def __update_product_to_db(self, _id, percent, desc, quantity, start_date, end_date):
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

    def search_discount(self, key):
        self.__discounts = []
        try:
            rows = Discount.select().where(fn.Lower(Discount.description).contains(fn.Lower(key)))
            self.__discounts.extend(rows)
            self.view.reload_treeview()
        except InternalError as px:
            print(str(px))

    def add_new_and_reload(self):
        values = self.view.get_detail_values()
        desc = values.get("description")
        percent = values.get("percent")
        start_date = values.get("start_date")
        end_date = values.get("end_date")
        quantity = values.get("quantity")
        if not self.is_not_validate(desc, percent, quantity):
            self.save_data_to_db(desc, percent, start_date, end_date, quantity)
            self.get_data()
            self.view.reload_treeview()

    def delete_and_reload(self):
        _id = self.view.item_treeview_selected()
        self.__delete_product(_id)
        self.get_data()
        self.view.reload_treeview()


    def update_and_reload(self):
        values = self.view.get_detail_values()
        desc = values.get("description")
        percent = values.get("percent")
        start_date = values.get("start_date")
        end_date = values.get("end_date")
        quantity = values.get("quantity")
        _id = self.view.id_selected
        if not self.is_not_validate(desc, percent, quantity):
            self.__update_product_to_db(_id, percent, desc, quantity, start_date, end_date)
            self.get_data()
            self.view.reload_treeview()

    def is_not_validate(self, description, percent, quantity):
        mess = None
        if not description or not percent or not quantity:
            mess = "Vui lòng nhập nội dung, số lượng, phần trăm khuyến mãi"
        if mess:
            messagebox.showinfo(message=mess)
        return mess
