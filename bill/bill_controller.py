from datetime import datetime
from tkinter import messagebox
import peewee
from bill.bill_view import BillView
from share.utils import Utils
from entities.models import Billing, User, Discount, Table, OrderList
from share.common_config import BillType, BillStatus, StatusTable


class BillController:
    def __init__(self, window):
        self.__bills = []
        self.get_all_bill()
        self.__view = BillView(window, self)

    @property
    def bills(self):
        return self.__bills

    def get_all_bill(self):
        self.__bills = []
        try:
            self.table_exits()
            results = Billing.select().order_by(Billing.createdDate.desc())
            if results:
                self.__bills.extend(results)
        except peewee.InternalError as px:
            print(str(px))
        return self.__bills

    def get_data_by_date(self, by_date):
        try:
            self.table_exits()
            results = Billing.select().where(Billing.createdDate.year == by_date.year
                                             and Billing.createdDate.month == by_date.month
                                             and Billing.createdDate.day == by_date.day)

            if results:
                return results
        except peewee.InternalError as px:
            print(str(px))

    def save_data_to_db(self, user_id, customer_name, customer_phone, money, bill_type, created_date, status_bill):
        try:
            self.table_exits()
            row = Billing(userId=user_id,
                          customerName=customer_name,
                          customerPhoneNumber=customer_phone,
                          totalMoney=money,
                          type=bill_type,
                          status=status_bill,
                          createdDate=created_date)

            bill = row
            bill.save()
            pass
        except peewee.InternalError as px:
            messagebox.showinfo("Thông báo", "Thêm sản phẩm thất bại. Vui lòng thử lại.")
            print(str(px))

    def __delete_bill(self, bill_id):
        try:
            self.table_exits()
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
        except peewee.InternalError as px:
            print(str(px))

    def __update_bill_to_db(self, id, create_date, customer_name, customer_phone, money, bill_type, status_bill):
        try:
            self.table_exits()
            b: Billing = Billing.get(Billing.id == id)
            b.customerName = customer_name
            b.customerPhoneNumber = customer_phone
            b.money = money
            b.type = bill_type
            b.createdDate = create_date
            b.status = status_bill
            b.updatedDate = datetime.now()
            b.save()
        except peewee.InternalError as px:
            print(str(px))

    def add_new_bill_and_reload(self, bill_id):
        b = Billing.get_or_none(Billing.id == bill_id)
        if b:
            messagebox.showinfo(message=f"Hóa đơn ID ({b.id}) đã tồn tại")
            return
        detail_form_values = self.__view.get_detail_form_values()
        user_id = Utils.user_profile["id"]
        customer_name = detail_form_values.get("customerName")
        customer_phone = detail_form_values.get("customerPhoneNumber")
        money = detail_form_values.get("totalMoney")
        created_date = detail_form_values.get('created_date')
        status_bill = detail_form_values.get("status_bill")
        bill_type = detail_form_values.get("bill_type")
        self.save_data_to_db(user_id, customer_name,
                             customer_phone, money, bill_type, created_date, status_bill)
        self.get_all_bill()

    def delete_and_reload(self, _id):
        self.__delete_bill(_id)
        self.get_all_bill()

    def update_and_reload(self, _id):
        detail_form_values = self.__view.get_detail_form_values()
        customer_name = detail_form_values.get("customerName")
        customer_phone = detail_form_values.get("customerPhoneNumber")
        money = detail_form_values.get("totalMoney")
        bill_type = detail_form_values.get("bill_type")
        status_bill = detail_form_values.get("status_bill")
        created_date = detail_form_values.get("created_date")
        self.__update_bill_to_db(_id, created_date, customer_name, customer_phone, money, bill_type, status_bill)
        self.get_all_bill()

    def get_tables(self):
        tables = []
        try:
            rows = Table.select()
            tables.extend(rows)
        except peewee.InternalError as px:
            print(str(px))

        ids = iter([i.id for i in tables])
        tb_nums = iter([i.tableNum for i in tables])
        _dict = dict(zip(ids, tb_nums))
        return _dict

    def get_user_name_by_id(self, _id):
        try:
            u = User.table_exists()
            if not u:
                User.create_table()
            user: User = User.get_or_none(User.id == _id)
            if user:
                return user.user_name
        except peewee.InternalError as px:
            print(str(px))

    def get_table_num_by_id(selfs, _id):
        try:
            t = Table.table_exists()
            if not t:
                Table.create_table()
            t: Table = Table.get_or_none(Table.id == _id)
            if t:
                return t.tableNum
        except peewee.InternalError as px:
            print(str(px))

    def table_exits(self):
        b = Billing.table_exists()
        if not b:
            Billing.create_table()
