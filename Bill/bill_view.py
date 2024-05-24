from datetime import datetime
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as bt

class BillView:
    def __init__(self, window, controller):
        self.__controller = controller
        self.__generate_ui_content(window)

    def __generate_ui_content(self, window):
        style = ttk.Style()
        style.theme_use('default')

        main_fr = ttk.Frame(window)
        main_fr.pack(fill=tk.BOTH, expand=1)

        date_fr = ttk.Frame(main_fr)
        date_fr.pack(fill=tk.BOTH, expand=0, pady=10, padx=20)

        lb_date = ttk.Label(date_fr, text="Ngày tạo")
        lb_date.grid(row=0, column=0)
        self.date_value = tk.StringVar()
        self.date_value.set(f"{datetime.now():%d/%m/%Y}")
        self.date_entry = bt.DateEntry(date_fr, dateformat="%d/%m/%Y", bootstyle="primary")
        self.date_entry.entry.configure(textvariable=self.date_value)
        self.date_value.trace('w', lambda name, index, mode, date_value=self.date_value: self.change_date_reload_view())
        self.date_entry.grid(row=0, column=1)
        self.t = ttk.Treeview(main_fr)
        self.t.pack(fill=tk.BOTH, expand=1, padx=20, pady=10)

        style.configure("Treeview.Heading", background="#000099",
                              foreground="white")

        self.t["columns"] = ("id", "user_create", "create_date", "customer_name", "customer_phone", "table_num", "total_money")
        self.t["show"] = "headings"
        self.t.column("id", anchor="center", width=80)
        self.t.column("user_create", anchor="center")
        self.t.column("customer_name", anchor="center")
        self.t.column("customer_phone", anchor="center", width=200)
        self.t.column("table_num", anchor="center", width=100)
        self.t.column("total_money", anchor="center")
        self.t.column("create_date", anchor="center", width=200)

        self.t.heading("id", text="ID")
        self.t.heading("user_create", text="Người Tạo")
        self.t.heading("create_date", text="Ngày Tạo")
        self.t.heading("customer_name", text="Tên Khách Hàng")
        self.t.heading("customer_phone", text="SDT Khách Hàng")
        self.t.heading("table_num", text="Số Bàn")
        self.t.heading("total_money", text="Tổng Tền")
        self.t.tag_configure("normal", background="white")
        self.t.tag_configure("blue", background="lightblue")
        self.__insert_column_values()

    def change_date_reload_view(self):
        for item in self.t.get_children():
            self.t.delete(item)
        if self.date_value.get() != '':
            self.__insert_column_values(datetime.strptime(self.date_value.get(), "%d/%m/%Y"))

    def __insert_column_values(self, by_date=datetime.now()):
        my_tag = "blue"
        bills = self.__controller.get_data(by_date)
        for bill in bills:
            if my_tag == "normal":
                my_tag = "blue"
            else:
                my_tag = "normal"
            self.t.insert("", "end", iid=bill.id, text=bill.id,
                          values=(bill.id, bill.userId, bill.createdDate, bill.customerName, bill.customerPhoneNumber,
                                  bill.tableId, bill.totalMoney),
                          tags=my_tag)

