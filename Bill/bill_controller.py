from datetime import datetime
from tkinter import messagebox
import peewee
from Bill.bill_model import Billing
from Bill.bill_view import BillView
from Table_Order.table_model import Table
from WareHouse.discount_model import Discount
from database.connection import Connection
from entities.models import User


class BillController:
    def __init__(self, window):
        self.__bills = []
        self.__view = BillView(window, self)

    @property
    def bills(self):
        return self.__bills

    def get_data(self, by_date):
        self.__bills = []
        try:
            Connection.db_handle.connect()
            b = Billing.table_exists()
            if not b:
                Billing.create_table()
            results = Billing.select().where(Billing.createdDate.year == by_date.year
                                             and Billing.createdDate.month == by_date.month
                                             and Billing.createdDate.day == by_date.day)

            self.__bills.extend(results)
        except peewee.InternalError as px:
            print(str(px))
        finally:
            Connection.db_handle.close()
        return self.__bills

    def save_data_to_db(self, table_id, user_id, creator_name, discount_id, customer_name, customer_phone, money, bill_type):
        try:
            Connection.db_handle.connect()
            pr = Billing.table_exists()
            if not pr:
                Billing.create_table()
            row = Billing(tableId=table_id,
                          userId=user_id,
                          discountId=discount_id,
                          customerName=customer_name,
                          customerPhoneNumber=customer_phone,
                          creatorName=creator_name,
                          totalMoney=money,
                          type=bill_type,
                          createdDate=datetime.now())
            row.save()
            messagebox.showinfo("Thông báo", "Thêm sản phẩm thành công")

        except peewee.InternalError as px:
            messagebox.showinfo("Thông báo", "Thêm sản phẩm thất bại. Vui lòng thử lại.")
            print(str(px))
        finally:
            Connection.db_handle.close()

    def __delete_bill(self, bill_id):
        try:
            Connection.db_handle.connect()
            product = Billing.get_or_none(Billing.id == bill_id)
            if product:
                product.delete_instance()
                messagebox.showinfo("Thông báo", "Xóa bàn thành công")
            else:
                print(f"No record found with ID {bill_id}")
                messagebox.showinfo("Thông báo", "Xóa bàn thất bại")
        except peewee.InternalError as px:
            print(str(px))
        finally:
            Connection.db_handle.close()

    def __update_bill_to_db(self, id, creator_name, create_date, customer_name, customer_phone, money, bill_type):
        try:
            Connection.db_handle.connect()
            b = Billing.get(Billing.id == id)
            b.creatorName = creator_name
            b.customerName = customer_name
            b.customerPhoneNumber = customer_phone
            b.money = money
            b.type = bill_type
            b.createdDate = create_date
            b.updatedDate = datetime.now()
            b.save()
            print(create_date)
            print("Update table success")
        except peewee.InternalError as px:
            print("Update table failure")
            print(str(px))
        finally:
            Connection.db_handle.close()
    def add_new_bill_and_reload(self):
        detail_form_values = self.__view.get_detail_form_values()
        table_num = detail_form_values.get("table_num")
        table_id = None
        user_id = None
        creator_name = detail_form_values.get("creator_name")
        discount_id = None
        customer_name = detail_form_values.get("customerName")
        customer_phone = detail_form_values.get("customerPhoneNumber")
        money = detail_form_values.get("totalMoney")
        bill_type = detail_form_values.get("bill_type")
        self.save_data_to_db(table_id, user_id, creator_name, discount_id, customer_name, customer_phone, money, bill_type)
        self.get_data(datetime.now())


    def delete_and_reload(self, _id):
        self.__delete_bill(_id)
        self.get_data(datetime.now())

    def update_and_reload(self, _id):
        detail_form_values = self.__view.get_detail_form_values()
        creator_name = detail_form_values.get("creator_name")
        customer_name = detail_form_values.get("customerName")
        customer_phone = detail_form_values.get("customerPhoneNumber")
        money = detail_form_values.get("totalMoney")
        bill_type = detail_form_values.get("bill_type")
        created_date = detail_form_values.get("created_date")
        self.__update_bill_to_db(_id, creator_name, created_date, customer_name,customer_phone, money, bill_type)
        self.get_data(datetime.now())

    def get_tables(self):
        tables = []
        try:
            Connection.db_handle.connect()
            t = Table.table_exists()
            if not t:
                Table.create_table()
            results = Table.select()
            tables.extend(results)
        except peewee.InternalError as px:
            print(str(px))
        finally:
            Connection.db_handle.close()
        ids = iter([i.id for i in tables])
        tb_nums = iter([i.tableNum for i in tables])
        _dict = dict(zip(ids, tb_nums))
        return _dict

    def get_discounts(self):
        discounts = []
        try:
            Connection.db_handle.connect()
            d = Discount.table_exists()
            if not d:
                Discount.create_table()
            results = Discount.select()
            discounts.extend(results)
        except peewee.InternalError as px:
            print(str(px))
        finally:
            Connection.db_handle.close()
        ids = iter([i.id for i in discounts])
        content = iter([f"{i.description} {i.percent}" for i in discounts])
        _dict = dict(zip(ids, content))
        return _dict

    def get_user_name_by_id(self, _id):
        user_name = None
        try:
            Connection.db_handle.connect()
            u = User.table_exists()
            if not u:
                User.create_table()
            row = User.select().where(User.id == _id)
            if row:
                if row.last_name and row.first_name:
                    user_name = row.user_name
                else:
                    user_name = f"{row.first_name} {row.last_name}"
        except peewee.InternalError as px:
            print(str(px))
        finally:
            Connection.db_handle.close()
        return user_name
