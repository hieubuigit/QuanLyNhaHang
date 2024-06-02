from datetime import datetime
import peewee
from table_order.menu_food_view import MenuFoodView
from entities.models import Product, Billing, Table, OrderList, Discount
from tkinter import messagebox

from share.common_config import BillType, BillStatus, StatusTable


class MenuFoodController:
    def __init__(self, parent, reload_table_page, table: Table = None):
        self.__foods = []
        self.__table = table
        self.__bill_id = None

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
        try:
            if not Product.table_exists():
                Product.create_table()
            rows = Product().select()
            self.__foods = rows
        except peewee.InternalError as px:
            print(str(px))

    def get_order_list_by_id(self):
        try:
            if self.__table:
                if Billing.table_exists():
                    bill = Billing.get_or_none(Billing.tableId == self.__table.id, Billing.status == BillStatus.UNPAID.value)
                    if bill:
                        self.bill_id = bill.id
                        if OrderList.table_exists():
                            order_list = OrderList.select().where(OrderList.billing_id == bill.id)
                            return order_list
                        else:
                            OrderList.create_table()
                            return None
                else:
                    Billing.create_table()
        except peewee.InternalError as px:
            print(str(px))

    def create_order_list(self, food: Product, quantity_selected):
        try:
            if self.bill_id:
                if OrderList.table_exists():
                    pr = OrderList.get_or_none(OrderList.billing_id == self.__bill_id,
                                               OrderList.product_id == food.id)
                    if pr:
                        messagebox.showinfo("Thông báo", "Món ăn đã có trong hóa đơn")
                        return
                    bill = Billing.get(self.bill_id == Billing.id)
                    product = self.get_product_by_id(food.id)
                    row = OrderList()
                    row.billing_id = bill
                    row.product_id = product
                    row.cur_price = food.price
                    row.quantity = quantity_selected
                    row.created_date = datetime.now
                    row.save()
                else:
                    OrderList.create_table()

        except peewee.InternalError as px:
            print(str(px))

    def get_product_by_id(self, _id):
        try:
            product: Product = Product.get_by_id(_id)
            return product
        except peewee.InternalError as px:
            print(str(px))

    def delete_order_list_by_id(self, _id):
        try:
            return OrderList.delete_by_id(_id)
        except peewee.InternalError as px:
            print(str(px))

    def update_quantity(self, order_list_id, new_quantity, cur_price):
        try:
            row = OrderList.get_or_none(OrderList.id == order_list_id)
            if row:
                row.quantity = new_quantity
                row.cur_price = cur_price
                row.save()
                return 1
        except peewee.InternalError as px:
            print(str(px))

    def get_discount_percents(self):
        try:
            if Discount.table_exists():
                rows = Discount.select()
                if rows:
                    percent_list = [f"{i.percent:.0f}" for i in rows]
                    return percent_list
        except peewee.InternalError as px:
            print(str(px))

    def update_bill(self, total_money):
        print("bill id", self.__bill_id)
        try:
            bill = Billing.get_or_none(Billing.id == self.__bill_id)
            if bill:
                bill.totalMoney = total_money
                bill.type = BillType.REVENUE.value[0]
                bill.status = BillStatus.PAID.value
                bill.updatedDate = datetime.now()
                bill.save()
                return 1
        except peewee.InternalError as px:
            print(str(px))
