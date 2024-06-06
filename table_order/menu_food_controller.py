from datetime import datetime
import peewee
from table_order.menu_food_view import MenuFoodView
from entities.models import Product, Billing, Table, OrderList, Discount
from tkinter import messagebox

from share.common_config import BillType, BillStatus, StatusTable
from table_order.order_model import OrderModel


class MenuFoodController:
    def __init__(self, parent, reload_table_page, table: Table = None):
        self.__foods = []
        self.__table = table
        self.__bill_id = None
        self._order_model = OrderModel()
        self.get_foods()
        view = MenuFoodView(parent, self, reload_table_page, table)


    @property
    def foods(self):
        return self.__foods

    @foods.setter
    def foods(self, value):
        self.__foods = value

    @property
    def bill_id(self):
        return self.__bill_id

    @bill_id.setter
    def bill_id(self, value):
        self.__bill_id = value

    def get_foods(self):
        rows = self._order_model.get_foods()
        if rows:
            self.__foods = rows

    def get_order_list_by_id(self):
        if self.__table:
            bill = self._order_model.get_bill_by_table_id(self.__table.id)
            if bill:
                self.bill_id = bill.id
                return self._order_model.get_order_list_by_bill_id(bill_id=bill.id)

    def create_order_list(self, food: Product, quantity_selected):
        if self.bill_id:
            order = self._order_model.get_order_list_by(bill_id=self.bill_id, product_id=food.id)
            if order:
                messagebox.showinfo("Thông báo", "Món ăn đã có trong hóa đơn")
                return
            self._order_model.create_order_list(bill_id=self.bill_id, food=food, quantity_selected=quantity_selected)

    def delete_order_list_by_id(self, _id):
        return self._order_model.delete_order_list_by(_id)

    def update_quantity(self, order_list_id, new_quantity, cur_price):
        result = self._order_model.update_row_order_list(order_list_id, new_quantity, cur_price)
        return result

    def get_discount_percents(self):
        return self._order_model.get_discount()

    def update_bill(self, total_money, customer_name, customer_phone):
       result = self._order_model.update_bill_to_db(self.bill_id, total_money, customer_name, customer_phone)
       return result

    def get_products_by_id(self, id):
        return self._order_model.get_products_by_id(id)