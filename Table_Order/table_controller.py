import datetime
import tkinter as tk
from tkinter import messagebox

import peewee

from Bill.bill_model import Billing
from Table_Order.menu_food_controller import MenuFoodController
from Table_Order.table_model import *
from Table_Order.table_view import TableView
from database.connection import Connection
from share.common_config import UserType


class TableController:
    def __init__(self, window):
        self.__data_table = []
        self.__user_type = UserType.NORMAL
        self.root = window
        self.__get_table_data()
        self.view = TableView(window, self, self.__user_type)

    @property
    def tables(self):
        return self.__data_table

    def __get_table_data(self):
        self.__data_table = []
        try:
            Connection.db_handle.connect()
            results = Table.select()
            if len(results) > 0:
                self.__data_table.extend(results)
            if self.__user_type == UserType.ADMIN:
                self.__data_table.insert(0, Table(tableNum="+", table_type=TableType.Add))
            print(f"get data: {len(self.__data_table)}")
        except peewee.InternalError as px:
            print(str(px))
        finally:

            Connection.db_handle.close()
            print("db is close table when get sucess", Connection.db_handle.is_closed())

    def add_new_table_to_db(self, table_num, seat_num, status):
        try:
            Connection.db_handle.connect()
            row_table = Table(tableNum=table_num, seatNum=seat_num, status=status, createdDate=datetime.datetime.now())
            row_table.save()
            print("Save table success")
        except peewee.InternalError as px:
            print("Save table failure")
            print(str(px))
        finally:
            Connection.db_handle.close()

    def update_table_to_db(self, id, table_num, seat_num, status):
        try:
            Connection.db_handle.connect()
            table = Table.get(Table.id == id)
            table.tableNum = table_num
            table.seatNum = seat_num
            table.status = status
            table.updatedDate = datetime.datetime.now()
            table.save()
            print("Update table success")
        except peewee.InternalError as px:
            print("Update table failure")
            print(str(px))
        finally:
            Connection.db_handle.close()

    def update_table_status(self, id_table, status):
        try:
            Connection.db_handle.connect()
            table = Table.get(Table.id == id)
            table.status = status
            table.save()
            print("Update table success")
        except peewee.InternalError as px:
            print("Update table failure")
            print(str(px))
        finally:
            Connection.db_handle.close()

    def __delete_table(self, table_id):
        try:
            Connection.db_handle.connect()
            table = Table.get_or_none(Table.id == table_id)
            if table:
                table.delete_instance()
                messagebox.showinfo("Thông báo", "Xóa bàn thành công")
            else:
                print(f"No record found with ID {table_id}")
                messagebox.showinfo("Thông báo", "Xóa bàn thất bại")
        except peewee.InternalError as px:
            print(str(px))
        finally:
            Connection.db_handle.close()

    def delete_and_reload(self, table_id):
        self.__delete_table(table_id)
        self.__get_table_data()


    def add_new_and_reload(self, table_num_value, seat_num_value, status_value):
        self.add_new_table_to_db(table_num_value, seat_num_value, status_value)
        self.__get_table_data()

    def update_and_reload(self, id, table_num_value, seat_num_value, status_value):
        self.update_table_to_db(id, table_num_value, seat_num_value, status_value)
        self.__get_table_data()

    def save_bill(self):
        try:
            Connection.db_handle.connect()
            b = Billing()
            b.save()
            print("Save bill success")
        except peewee.InternalError as px:
            print("Update bill failure")
            print(str(px))
        finally:
            Connection.db_handle.close()

    def update_bill(self, id_bill, quantity):
        try:
            Connection.db_handle.connect()
            b = Billing()
            b.save()
            print("Save bill success")
        except peewee.InternalError as px:
            print("Update bill failure")
            print(str(px))
        finally:
            Connection.db_handle.close()

    def show_menu_food(self, view_master):
        print("db is close table at show menu", Connection.db_handle.is_closed())
        menu = MenuFoodController(view_master)

