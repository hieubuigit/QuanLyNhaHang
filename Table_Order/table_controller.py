from datetime import datetime
from tkinter import messagebox
import peewee
from Table_Order.menu_food_controller import MenuFoodController
from Table_Order.table_model import TableModel
from Table_Order.table_view import TableView
from entities.models import User, Table, Billing
from share.common_config import UserType, TableType, BillType, BillStatus
from share.utils import Utils


class TableController:
    def __init__(self, window):
        self.__data_table = []
        self.__user_type = Utils.user_profile["type"]
        print(self.__user_type)
        self.root = window
        self.__get_table_data()
        self.view = TableView(window, self, self.__user_type)

    @property
    def tables(self):
        return self.__data_table

    def __get_table_data(self):
        self.__data_table = []
        self.__table_model = TableModel()
        tables = self.__table_model.get_data()
        if tables:
            self.__data_table.extend(tables)
        if self.__user_type == UserType.ADMIN.value:
            self.__data_table.insert(0, Table(tableNum="+", table_type=TableType.Add))

    def add_new_table_to_db(self, table_num, seat_num, status):
        try:
            if not Table.table_exists():
                Table.create_table()
            row_table = Table(tableNum=table_num, seatNum=seat_num, status=status, createdDate=datetime.now())
            row_table.save()
            print("Save table success")
        except peewee.InternalError as px:
            print("Save table failure")
            print(str(px))


    def update_table_to_db(self, id, table_num, seat_num, status):
        try:
            if not Table.table_exists():
                Table.create_table()
            table = Table.get(Table.id == id)
            table.tableNum = table_num
            table.seatNum = seat_num
            table.status = status
            table.updatedDate = datetime.now()
            table.save()
            print("Update table success")
        except peewee.InternalError as px:
            print("Update table failure")
            print(str(px))


    def update_table_status(self, id_table, status):
        try:
            if not Table.table_exists():
                Table.create_table()
            table = Table.get(Table.id == id_table)
            table.status = status
            table.save()
            self.__get_table_data()
            return 1
        except peewee.InternalError as px:
            print(str(px))


    def __delete_table(self, table_id):
        try:

            if not Table.table_exists():
                Table.create_table()
            table = Table.get_or_none(Table.id == table_id)
            if table:
                table.delete_instance()
                messagebox.showinfo("Thông báo", "Xóa bàn thành công")
            else:
                print(f"No record found with ID {table_id}")
                messagebox.showinfo("Thông báo", "Xóa bàn thất bại")
        except peewee.InternalError as px:
            print(str(px))

    def create_bill(self, id_table, id_user):
        try:
            user = User.get(User.id == id_user)
            table = Table.get(Table.id == id_table)
            if not Billing.table_exists():
                Billing.create_table()
            b = Billing()
            b.tableId = table
            b.userId = user
            b.type = BillType.REVENUE.value[0]
            b.status = BillStatus.UNPAID.value
            b.createdDate = datetime.now()
            b.save()
        except peewee.InternalError as px:
            print(str(px))
    def delete_and_reload(self, table_id):
        self.__delete_table(table_id)
        self.__get_table_data()


    def add_new_and_reload(self, table_num_value, seat_num_value, status_value):
        self.add_new_table_to_db(table_num_value, seat_num_value, status_value)
        self.__get_table_data()

    def update_and_reload(self, id, table_num_value, seat_num_value, status_value):
        self.update_table_to_db(id, table_num_value, seat_num_value, status_value)
        self.__get_table_data()



    def show_menu_food(self, view_master, table, reload_table_page):
        menu = MenuFoodController(view_master, reload_table_page, table=table)




