from datetime import datetime
from tkinter import messagebox

from peewee import fn, InternalError

from warehouse.discount_model import DiscountModel
from warehouse.discount_view import DiscountView
from entities.models import Discount


class DiscountController:
    def __init__(self, root):
        self.__discounts = []
        self._discount_model = DiscountModel()
        self.get_data()
        self.view = DiscountView(root=root, controller=self)

    @property
    def discounts(self):
        return self.__discounts

    def get_data(self):
        self.__discounts = []
        rows = self._discount_model.get_discounts()
        if rows:
            self.__discounts.extend(rows)

    def search_discount(self, key):
        self.__discounts = []
        rows = self._discount_model.search_discounts(key)
        self.__discounts.extend(rows)
        self.view.reload_treeview()

    def add_new_and_reload(self):
        values = self.view.get_detail_values()
        desc = values.get("description")
        percent = values.get("percent")
        start_date = values.get("start_date")
        end_date = values.get("end_date")
        quantity = values.get("quantity")
        if not self.is_not_validate(desc, percent, quantity):
            self._discount_model.save_discount(desc, percent, start_date, end_date, quantity)
            self.get_data()
            self.view.reload_treeview()
            self.view.refresh_detail_form()

    def delete_and_reload(self):
        if messagebox.askokcancel(message="Bạn có chắc chắn xóa không?"):
            _id = self.view.id_selected
            self._discount_model.delete_discount(_id)
            self.get_data()
            self.view.reload_treeview()
            self.view.refresh_detail_form()

    def update_and_reload(self):
        values = self.view.get_detail_values()
        desc = values.get("description")
        percent = values.get("percent")
        start_date = values.get("start_date")
        end_date = values.get("end_date")
        quantity = values.get("quantity")
        _id = self.view.id_selected
        if not self.is_not_validate(desc, percent, quantity):
            self._discount_model.update_discount(_id, percent, desc, quantity, start_date, end_date)
            self.get_data()
            self.view.reload_treeview()
            self.view.refresh_detail_form()

    def is_not_validate(self, description, percent, quantity):
        mess = None
        if not description or not percent or not quantity:
            mess = "Vui lòng nhập nội dung, số lượng, phần trăm khuyến mãi"
        if mess:
            messagebox.showinfo(message=mess)
        return mess
