import tkinter as tk

from Table_Order.table_model import TableModel
from Table_Order.table_view import TableView
from database.connection import Connection


class TableController(tk.Frame):
    def __init__(self, window):
        super().__init__()
        self.__data_table = []
        self.__fetch_data()
        view = TableView(window, self.__data_table)
    def __fetch_data(self):
        connect = Connection()
        query = "SELECT * FROM QuanLyNhaHang.`Table`"
        results = connect.get(query)
        for row in results:
            self.__data_table.append(TableModel(id=row.get("Id"), table_num=row.get("TableNum"), seat_num=row.get("SeatNum"), status=row.get("Status")))
        connect.close()


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(True, True)
    root.state('zoomed')  # full screen
    root.title("Restaurant Information")
    home = TableController(root)
    root.mainloop()