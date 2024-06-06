import math

from report.report_model import ReportModel
from report.report_view import ReportView
from datetime import datetime, timedelta
import peewee
# from database.connection import Connection
from entities.models import User, Billing, Table
from share.common_config import BillType


class ReportController:
    def __init__(self, root):
        self.__total_revenue = 0
        self.__total_expend = 0
        self.__bills = []
        self.__months_of_the_quarter = None
        self._current_quarter = math.ceil(datetime.now().month / 3)
        self._report_model = ReportModel()
        self.__get_bills(self._current_quarter)
        self.view = ReportView(root, self)

    @property
    def total_revenue(self):
        return self.__total_revenue

    @property
    def total_expend(self):
        return self.__total_expend

    @total_expend.setter
    def total_expend(self, value):
        self.__total_expend = value

    @total_revenue.setter
    def total_revenue(self, value):
        self.__total_revenue = value

    @property
    def current_quarter(self):
        return self._current_quarter

    @property
    def bills(self):
        return self.__bills

    @property
    def months_of_the_quarter(self):
        return self.__months_of_the_quarter

    def __get_bills(self, quarter=1):
        self.__bills = []
        cur_quarter = quarter
        start_date = self.get_first_date_by_quarter(cur_quarter)
        end_date = self.get_last_date_by_quarter(cur_quarter, start_date)
        self.__months_of_the_quarter = [x for x in range(start_date.month, end_date.month + 1)]
        end_date = end_date + timedelta(days=1)
        results = self._report_model.get_bills(start_date, end_date)
        self.__bills.extend(results)

        # tính giá trị tổng thu, tổng chi theo quý
        self.total_revenue = sum(i.totalMoney for i in self.__bills if i.type == BillType.REVENUE.value[0])
        self.total_expend = sum(i.totalMoney for i in self.__bills if i.type == BillType.EXPANDING.value[0])

    def get_first_date_by_quarter(self, current_quarter):
        return datetime(datetime.now().year, current_quarter * 3 - 2, 1)

    def get_last_date_by_quarter(self, current_quarter, start_date):

        end_date = datetime(datetime.now().year, current_quarter * 3, 1)
        while True:
            far_future = start_date + timedelta(days=93)
            start_of_next_quarter = far_future.replace(day=1)
            end_of_quarter = start_of_next_quarter - timedelta(days=1)
            if end_of_quarter > end_date:
                break
        return end_of_quarter

    def get_bills_and_reload_view(self, quarter):
        self.__get_bills(quarter)
        self.view.reload_treeview()

    def get_user_name_by_id(self, _id):
        return self._report_model.get_user_name(_id)

    def get_table_num_by_id(self, _id):
        return self._report_model.get_table_num(_id)
