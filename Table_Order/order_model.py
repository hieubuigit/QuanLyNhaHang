from datetime import datetime

from peewee import Model, InternalError

from entities.models import Product, database, Billing, OrderList, Discount
from share.common_config import BillStatus, BillType


class OrderModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with database:
            database.create_tables([Product, Billing, OrderList, Discount], safe=True)

    def get_foods(self):
        try:
            rows = Product().select()
            return rows
        except InternalError as px:
            print(str(px))

    def get_bill_by_table_id(self, table_id):
        try:
            bill = Billing.get_or_none(Billing.tableId == table_id, Billing.status == BillStatus.UNPAID.value)
            return bill
        except InternalError as px:
            print(str(px))

    def get_order_list_by_bill_id(self, bill_id):
        try:
            if OrderList.table_exists():
                order_list = OrderList.select().where(OrderList.billing_id == bill_id)
                return order_list
            else:
                OrderList.create_table()
                return None
        except InternalError as px:
            print(str(px))

    def get_order_list_by(self, bill_id, product_id):
        try:
            order = OrderList.get_or_none(OrderList.billing_id == bill_id, OrderList.product_id == product_id)
            return order
        except InternalError as px:
            print(str(px))

    def create_order_list(self, bill_id, food: Product, quantity_selected):
        try:
            bill = Billing.get(bill_id == Billing.id)
            product = self.get_products_by_id(food.id)
            row = OrderList()
            row.billing_id = bill
            row.product_id = product
            row.cur_price = food.price
            row.quantity = quantity_selected
            row.created_date = datetime.now
            row.save()
        except InternalError as px:
            print(str(px))

    def get_products_by_id(self, id):
        try:
            product: Product = Product.get_by_id(id)
            return product
        except InternalError as px:
            print(str(px))

    def delete_order_list_by(self, _id):
        try:
            return OrderList.delete_by_id(_id)
        except InternalError as px:
            print(str(px))

    def update_row_order_list(self, order_list_id, new_quantity, cur_price):
        try:
            row = OrderList.get_or_none(OrderList.id == order_list_id)
            if row:
                row.quantity = new_quantity
                row.cur_price = cur_price
                row.save()
                return 1
        except InternalError as px:
            print(str(px))

    def get_discount(self):
        try:
            d = Discount.table_exists()
            if d:
                rows = Discount.select()
                if rows:
                    percent_list = [f"{i.percent:.0f}" for i in rows]
                    return percent_list
        except InternalError as px:
            print(str(px))

    def update_bill_to_db(self, bill_id, total_money, customer_name, customer_phone):
        try:
            bill: Billing = Billing.get_or_none(Billing.id == bill_id)
            if bill:
                bill.customerName = customer_name
                bill.customerPhoneNumber = customer_phone
                bill.totalMoney = total_money
                bill.type = BillType.REVENUE.value[0]
                bill.status = BillStatus.PAID.value
                bill.updatedDate = datetime.now()
                bill.save()
                return 1
        except InternalError as px:
            print(str(px))