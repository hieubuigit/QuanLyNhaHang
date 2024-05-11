import tkinter as tk
import peewee
from Table_Order.table_model import *
from Table_Order.table_view import TableView
from database.connection import Connection


class TableController:
    def __init__(self, window):
        self.__data_table = []
        self.__get_data()
        self.view = TableView(window, self, self.__data_table)

    def __get_data(self):
        try:
            Connection.db_handle.connect()
            results = Table.select()
            self.__data_table.extend(results)
        except peewee.InternalError as px:
            print(str(px))

        finally:
            Connection.db_handle.close()

    def add_table_to_db(self, table_num, seat_num, status):
        try:
            Connection.db_handle.connect()
            row_table = Table(tableNum=table_num, seatNum=seat_num, status=status)
            row_table.save()
            Connection.db_handle.close()
        except peewee.InternalError as px:
            print(str(px))

    def update_table_to_db(self, table_num, seat_num, status):
        try:
            Connection.db_handle.connect()
            table = Table.get(Table.id == id)
            table.tableNum = table_num
            table.seatNum = seat_num
            table.status = status
            table.save()
            Connection.db_handle.close()
        except peewee.InternalError as px:
            print(str(px))

    def save_table(self):
        self.add_table_to_db(self.view.table_num_value, self.view.seat_num_value, self.view.status_value)


# if __name__ == '__main__':
#     root = tk.Tk()
#     root.resizable(True, True)
#     root.state('zoomed')  # full screen
#     root.title("Restaurant Information")
#     root.config(background="blue")
#     home = TableController(root)
#     root.mainloop()