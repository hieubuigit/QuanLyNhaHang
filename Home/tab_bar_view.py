import sys
import os.path
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class TabBarView:
    path_assets = "{path_assets}".format(path_assets=os.getcwd().replace("Home", "assets"))
    button_type_clicked = ""

    def __init__(self, window):
        self.generate_tab_bar_view(window)

    def generate_tab_bar_view(self, parent):
        self.tab_bar_view = ttk.Frame(parent)
        self.tab_bar_view.place(height=35,rely=0)
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Custom.Normal.TButton', background='white', foreground='black', font=('Arial', 24))
        style.configure('Custom.CLiked.TButton', background='green', foreground='white', font=('Arial', 24))
        img_empl = ImageTk.PhotoImage(Image.open(
            "{path_assets}{img}".format(path_assets=TabBarView.path_assets, img="/password.png")).resize(
            (23, 23)))
        btn_size = (2, 2)
        self.empl_btn = ttk.Button(self.tab_bar_view, text="Nhân viên", style='Custom.Normal.TButton',
                                   image=img_empl, compound='left', padding=btn_size,
                                   command=lambda: self.action_tab(button_type='EMPLOYEE'))
        self.empl_btn.image = img_empl
        self.empl_btn.grid(row=0, column=0, sticky='nsw')

        img_table = ImageTk.PhotoImage(Image.open(
            "{path_assets}{img}".format(path_assets=TabBarView.path_assets, img="/password.png")).resize(
            (23, 23)))
        self.table_btn = ttk.Button(self.tab_bar_view, text="Đặt bàn", padding=btn_size, style='Custom.Normal.TButton',
                                    image=img_table, compound='left', command=lambda: self.action_tab(button_type="TABLE"))
        self.table_btn.image = img_table
        self.table_btn.grid(row=0, column=1)

        img_bill = ImageTk.PhotoImage(Image.open(
            "{path_assets}{img}".format(path_assets=TabBarView.path_assets, img="/password.png")).resize(
            (23, 23)))
        self.bill_btn = ttk.Button(self.tab_bar_view, text="Hóa đơn", padding=btn_size,
                             image=img_bill, style='Custom.Normal.TButton',
                             compound='left', command=lambda: self.action_tab(button_type='BILL'))
        self.bill_btn.image = img_bill
        self.bill_btn.grid(row=0, column=2)

        img_warehourse = ImageTk.PhotoImage(Image.open(
            "{path_assets}{img}".format(path_assets=TabBarView.path_assets, img="/password.png")).resize(
            (23, 23)))
        self.warehouse_btn = ttk.Button(self.tab_bar_view, text="Nhà kho", padding=btn_size,
                                   image=img_warehourse, style='Custom.Normal.TButton',
                                   compound='left', command=lambda: self.action_tab(button_type='WAREHOUSE'))
        self.warehouse_btn.image = img_warehourse
        self.warehouse_btn.grid(row=0, column=3)

        img_report = ImageTk.PhotoImage(Image.open(
            "{path_assets}{img}".format(path_assets=TabBarView.path_assets, img="/password.png")).resize(
            (23, 23)))
        self.report_btn = ttk.Button(self.tab_bar_view, text="Báo cáo", padding=btn_size, image=img_report, style='Custom.Normal.TButton',
                               compound='left', command=lambda: self.action_tab(button_type='REPORT'))
        self.report_btn.image = img_report
        self.report_btn.grid(row=0, column=4)

        img_logout = ImageTk.PhotoImage(Image.open(
            "{path_assets}{img}".format(path_assets=TabBarView.path_assets, img="/password.png")).resize(
            (23, 23)))
        self.logout_btn = ttk.Button(self.tab_bar_view, text="Đăng xuất", padding=btn_size,
                               image=img_logout, style='Custom.Normal.TButton',
                               compound='left', command=lambda: self.action_tab(button_type='LOGOUT'))
        self.logout_btn.image = img_logout
        self.logout_btn.grid(row=0, column=5)

        img_profile = ImageTk.PhotoImage(Image.open(
            "{path_assets}{img}".format(path_assets=TabBarView.path_assets, img="/password.png")).resize(
            (23, 23)))
        profile_btn = ttk.Button(parent, text="Addmin director",
                                image=img_profile,
                                compound='left')
        profile_btn.image = img_profile
        profile_btn.pack(side=tk.TOP, anchor=tk.NE)

    def action_tab(self, button_type):
        self.set_default_button()
        TabBarView.button_type_clicked = button_type
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Custom.CLiked.TButton', background='green', foreground='white', font=('Arial', 24))
        if button_type == "EMPLOYEE":
            self.empl_btn.config(style='Custom.CLiked.TButton')
        elif button_type == "TABLE":
            self.table_btn.config(style='Custom.CLiked.TButton')
        elif button_type == "BILL":
            self.bill_btn.config(style='Custom.CLiked.TButton')
        elif button_type == "WAREHOUSE":
            self.warehouse_btn.config(style='Custom.CLiked.TButton')
        elif button_type == "REPORT":
            self.report_btn.config(style='Custom.CLiked.TButton')
        elif button_type == "LOGOUT":
            self.logout_btn.config(style='Custom.CLiked.TButton')
    def set_default_button(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Custom.Normal.TButton', background='white', foreground='black', font=('Arial', 24))
        if TabBarView.button_type_clicked == "EMPLOYEE":
            self.empl_btn.config(style='Custom.Normal.TButton')
        elif TabBarView.button_type_clicked == "TABLE":
            self.table_btn.config(style='Custom.Normal.TButton')
        elif TabBarView.button_type_clicked == "BILL":
            self.bill_btn.config(style='Custom.Normal.TButton')
        elif TabBarView.button_type_clicked == "WAREHOUSE":
            self.warehouse_btn.config(style='Custom.Normal.TButton')
        elif TabBarView.button_type_clicked == "REPORT":
            self.report_btn.config(style='Custom.Normal.TButton')
        elif TabBarView.button_type_clicked == "LOGOUT":
            self.logout_btn.config(style='Custom.Normal.TButton')

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(True, True)
    root.state('zoomed')  # full screen
    root.title("Restaurant Information")

    home = TabBarView(root)

    root.mainloop()

