from datetime import datetime
from tkinter import messagebox
import peewee
from bill.bill_model import BillModel
from bill.bill_view import BillView
from table_order.table_model import TableModel
from entities.models import Billing
from share.common_config import BillType


class BillController:
    def __init__(self, window):
        self.__bills = []
        self.__bill_model = BillModel()
        self.__view = BillView(window, self)

    @property
    def bills(self):
        return self.__bills

    def get_data(self, by_date):
        self.__bills = []
        try:
            bills = self.__bill_model.get_bills_by_date(by_date)
            if bills:
                self.__bills.extend(bills)
        except peewee.InternalError as px:
            print(str(px))
        return self.__bills

    def save_data_to_db(self, table_id, user_id, creator_name, discount_id,
                        customer_name, customer_phone, money, bill_type, created_date):
        try:
            row = Billing(tableId=table_id,
                          userId=user_id,
                          discountId=discount_id,
                          customerName=customer_name,
                          customerPhoneNumber=customer_phone,
                          creatorName=creator_name,
                          totalMoney=money,
                          type=bill_type,
                          createdDate=created_date)
            self.__bill_model.save_bill(row)
            pass
        except peewee.InternalError as px:
            messagebox.showinfo("Thông báo", "Thêm sản phẩm thất bại. Vui lòng thử lại.")
            print(str(px))


    def __delete_bill(self, bill_id):
        try:
            if self.__bill_model.delete_by_id(bill_id):
                messagebox.showinfo("Thông báo", "Xóa bàn thành công")
            else:
                print(f"No record found with ID {bill_id}")
                messagebox.showinfo("Thông báo", "Xóa bàn thất bại")
        except peewee.InternalError as px:
            print(str(px))


    def __update_bill_to_db(self, id, creator_name, create_date, customer_name, customer_phone, money, bill_type):
        try:
            self.__bill_model.update_by_id(id, creator_name, create_date,
                                           customer_name, customer_phone, money, bill_type)
            print("Update bill success")
        except peewee.InternalError as px:
            print("Update bill failure")
            print(str(px))

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
        created_date = detail_form_values.get('created_date')
        bill_type = 0 if detail_form_values.get("bill_type") == BillType.REVENUE.value[1] else 1
        self.save_data_to_db(table_id, user_id, creator_name, discount_id, customer_name,
                             customer_phone, money, bill_type, created_date)
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
        table_model = TableModel()
        tables = []
        try:
            rows = table_model.get_data()
            tables.extend(rows)
        except peewee.InternalError as px:
            print(str(px))

        ids = iter([i.id for i in tables])
        tb_nums = iter([i.tableNum for i in tables])
        _dict = dict(zip(ids, tb_nums))
        return _dict

    def get_discounts(self):
        discounts = []
        try:
            rows = self.__bill_model.get_discount()
            discounts.extend(rows)
        except peewee.InternalError as px:
            print(str(px))

        ids = iter([i.id for i in discounts])
        content = iter([f"{i.description} {i.percent}" for i in discounts])
        _dict = dict(zip(ids, content))
        return _dict

    def get_user_name_by_id(self, _id):
        user_name = None
        try:
            user = self.__bill_model.get_user_by_id(_id)
            if user:
                if user.last_name and user.first_name:
                    user_name = user.user_name
                else:
                    user_name = f"{user.first_name} {user.last_name}"
        except peewee.InternalError as px:
            print(str(px))

        return user_name
