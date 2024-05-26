from datetime import datetime
from tkinter import messagebox

import peewee
from WareHouse.discount_model import Discount
from WareHouse.discount_view import DiscountView
from database.connection import Connection


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
            Connection.db_handle.connect()
            # Discount.drop_table()
            pr = Discount.table_exists()
            if not pr:
                Discount.create_table()
            rows = Discount.select()
            self.__discounts.extend(rows)
            print("Get product success")
        except peewee.InternalError as px:
            print("Get product failure")
            print(str(px))
        finally:
            Connection.db_handle.close()

    def save_data_to_db(self, desc, percent, start_date, end_date, quantity):
        try:
            Connection.db_handle.connect()
            pr = Discount.table_exists()
            if not pr:
                Discount.create_table()
            row = Discount(description=desc, percent=percent, start_date=start_date, end_date=end_date,
                           quantity=quantity, created_date=f"{datetime.now():%Y-%m-%d}")
            row.save()
            messagebox.showinfo("Thông báo", "Thêm sản phẩm thành công")
        except peewee.InternalError as px:
            messagebox.showinfo("Thông báo", "Thêm sản phẩm thất bại. Vui lòng thử lại.")
            print(str(px))
        finally:
            Connection.db_handle.close()

    def __delete_product(self, _id):
        try:
            Connection.db_handle.connect()
            product = Discount.get_or_none(Discount.id == _id)
            if product:
                product.delete_instance()
                messagebox.showinfo("Thông báo", "Xóa bàn thành công")
            else:
                print(f"No record found with ID {_id}")
                messagebox.showinfo("Thông báo", "Xóa bàn thất bại")
        except peewee.InternalError as px:
            print(str(px))
        finally:
            Connection.db_handle.close()

    def __update_product_to_db(self, _id, percent, desc, quantity, start_date, end_date):
        try:
            Connection.db_handle.connect()
            discount = Discount.get(Discount.id == _id)
            discount.percent = percent
            discount.description = desc
            discount.quantity = quantity
            discount.start_date = start_date
            discount.end_date = end_date
            discount.update_date = datetime.now()
            discount.save()
            print("Update success")
        except peewee.InternalError as px:
            print("Update failure")
            print(str(px))
        finally:
            Connection.db_handle.close()

    def add_new_and_reload(self):
        values = self.view.get_detail_values()
        desc = values.get("description")
        percent = values.get("percent")
        start_date = values.get("start_date")
        end_date = values.get("end_date")
        quantity = values.get("quantity")
        print(values)
        self.save_data_to_db(desc, percent, start_date, end_date, quantity)
        self.get_data()
        self.view.reload_treeview()

    def delete_and_reload(self):
        _id = self.view.item_treeview_selected()
        self.__delete_product(_id)
        self.get_data()
        self.view.reload_treeview()


    def update_and_reload(self):
        _id = self.view.item_treeview_selected()
        values = self.view.get_detail_values()
        desc = values.get("description")
        percent = values.get("percent")
        start_date = values.get("start_date")
        end_date = values.get("end_date")
        quantity = values.get("quantity")
        self.__update_product_to_db(_id, percent, desc, quantity, start_date, end_date)
        self.get_data()
        self.view.reload_treeview()
