from datetime import datetime
from tkinter import messagebox
import peewee

from bill.bill_model import BillModel
from bill.bill_view import BillView
from share.utils import Utils
from entities.models import Billing, User, Discount, Table, OrderList
from share.common_config import BillType, BillStatus, StatusTable, UserType


class BillController:
    def __init__(self, window):
        self.__bills = []
        self._user_type = Utils.user_profile["type"]
        self._bill_model = BillModel()
        self.get_all_bill()
        self.__view = BillView(window, self)

    @property
    def bills(self):
        return self.__bills

    def get_all_bill(self):
        self.__bills = []
        rows = self._bill_model.get_bills_by_user_type(self._user_type)
        if rows:
            self.bills.extend(rows)
        return self.__bills

    def get_data_by_date(self, by_date):
        self.__bills = []
        rows = self._bill_model.get_bill_by_date(by_date)
        if rows:
            self.bills.extend(rows)

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
        self._bill_model.save_bill(user_id, customer_name, customer_phone, money, bill_type, created_date, status_bill)
        self.get_all_bill()

    def delete_and_reload(self, _id):
        self._bill_model.delete_bill(_id)
        self.get_all_bill()

    def update_and_reload(self, _id):
        detail_form_values = self.__view.get_detail_form_values()
        customer_name = detail_form_values.get("customerName")
        customer_phone = detail_form_values.get("customerPhoneNumber")
        money = detail_form_values.get("totalMoney")
        bill_type = detail_form_values.get("bill_type")
        status_bill = detail_form_values.get("status_bill")
        created_date = detail_form_values.get("created_date")
        self._bill_model.update_bill(_id, created_date, customer_name, customer_phone, money, bill_type, status_bill)
        self.get_all_bill()

    def get_user_name_by_id(self, _id):
        return self._bill_model.get_user_name(_id)

    def get_table_num_by_id(self, _id):
        return self._bill_model.get_table_num(_id)

