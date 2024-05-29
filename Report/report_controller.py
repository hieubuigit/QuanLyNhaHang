from Report.report_view import ReportView
from datetime import datetime
from tkinter import messagebox
import peewee
from Bill.bill_model import Billing
from Bill.bill_view import BillView
from Table_Order.table_model import Table
from WareHouse.discount_model import Discount
from database.connection import Connection
from entities.models import User


class ReportController:
    def __init__(self, root):
        view = ReportView(root, self)
        self.total_revenue = 0
        self.total_expanding = 0

    def get_bills(self):
        bills = []
        try:
            Connection.db_handle.connect()
            b = Billing.table_exists()
            if not b:
                Billing.create_table()
            results = Billing.select()
            bills.extend(results)
        except peewee.InternalError as px:
            print(str(px))
        finally:
            Connection.db_handle.close()
            total_revenue = sum(float(i.totalMoney) for i in bills if i.type == 0)
            print(f"TT: {total_revenue:.0f}")
            self.total_expanding = sum(float(i.totalMoney) for i in bills if i.type == 1)
            print(f"TC {self.total_expanding:.0f}")
        return bills
        # TÍNH TÔNHR THU, TỔNG CHI, hiển thị chart
    def cal_revenue_total(self, total_money):
        total = 0
        total += total_money
        return total
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

