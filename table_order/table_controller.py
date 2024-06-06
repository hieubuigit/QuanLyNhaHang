from datetime import datetime
from tkinter import messagebox
import peewee
from table_order.menu_food_controller import MenuFoodController
from table_order.table_model import TableModel
from table_order.table_view import TableView
from entities.models import User, Table, Billing
from share.common_config import UserType, TableType, BillType, BillStatus
from share.utils import Utils


class TableController:
    def __init__(self, window):
        self.__data_table = []
        self.__user_type = Utils.user_profile["type"]
        self.root = window
        self._table_model = TableModel()
        self.__get_table_data()
        self.view = TableView(window, self, self.__user_type)

    @property
    def tables(self):
        return self.__data_table

    def __get_table_data(self):
        self.__data_table = []
        results = self._table_model.get_tables()
        if results:
            self.__data_table.extend(results)
        if self.__user_type == UserType.ADMIN.value:
            self.__data_table.insert(0, Table(tableNum="+", table_type=TableType.Add))

    def __update_table(self, id, table_num, seat_num, status):
        if self._table_model.update_table(id, table_num, seat_num, status) is None:
            messagebox.showinfo("", "Số bàn này đã tồn tại")
        else:
            return 1

    def update_table_status(self, id_table, status):
        self._table_model.update_table_status(id_table, status)
        self.__get_table_data()
        return 1

    def __delete_table(self, table_id):
        if self._table_model.delete_table(table_id=table_id):
            messagebox.showinfo("Thông báo", "Xóa bàn thành công")
        else:
            messagebox.showinfo("Thông báo", "Xóa bàn thất bại")

    def create_bill(self, id_table, id_user):
        return self._table_model.create_bill_by_table(id_table, id_user)

    def check_my_bill(self, table_id):
        if self._table_model.is_my_bill(table_id) is None:
            messagebox.showinfo(message="Bàn này đã được đặt và tạo hóa đơn bởi nhân viên khác")
        else:
            return 1

    def delete_and_reload(self, table_id):
        self.__delete_table(table_id)
        self.__get_table_data()

    def add_new_and_reload(self, table_num_value, seat_num_value, status_value):
        if self._table_model.get_table_by_table_num(table_num_value):
            messagebox.showinfo("", "Số bàn này đã tồn tại")
            return
        self._table_model.add_new_table(table_num_value, seat_num_value, status_value)
        self.__get_table_data()
        return 1

    def update_and_reload(self, id, table_num_value, seat_num_value, status_value):
        if self.__update_table(id, table_num_value, seat_num_value, status_value):
            self.__get_table_data()
            return 1

    def show_menu_food(self, view_master, table, reload_table_page):
        menu = MenuFoodController(view_master, reload_table_page, table=table)




