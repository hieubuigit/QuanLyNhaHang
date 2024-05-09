import os
import tkinter as tk
from enum import Enum
from tkinter import ttk
from PIL import Image, ImageTk
from Table_Order.table_controller import TableController
from employee_view import EmployeeView

class TabType(Enum):
    EMPLOYEE = "EMPLOYEE"
    TABLE = "TABLE"
    BILL = "BILL"
    REPORT = "REPORT"
    LOGOUT = "LOGOUT"
    WARE_HOUSE = "WARE_HOUSE"
class HomeView:
    button_type_clicked = None
    size_icon_tab = (28, 28)
    def __init__(self, window):
        # tạo frame thanh tab bar
        self.__root = window
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Custom.Normal.TButton', background='white', foreground='black', font=('Arial', 24))
        style.configure('Custom.CLiked.TButton', background='#003BC6', foreground='white', font=('Arial', 24))
        self.__generate_ui_header(window)
        # Tạo một frame chính để chuyển đổi nhiều frame
        self.__main_fr = ttk.Frame(window)
        self.__main_fr.pack(fill="both", expand=1)

        # Tab 1: Hiển thị pgae nhân viên
        self.employee_page(self.__main_fr)

    def __generate_ui_header(self, window):
        header_view = ttk.Frame(window)
        header_view.pack(fill="both", expand=0)
        self.tab_bar_view = ttk.Frame(header_view)
        self.tab_bar_view.pack(side="left")
        avt_default = ImageTk.PhotoImage(Image.open("../assets/avatar_default_man.png").resize(
            (30, 30)))
        profile_btn = ttk.Button(header_view, text="Admin director",
                                 style='Custom.Normal.TButton',
                                 image=avt_default,
                                 compound='right')
        profile_btn.image = avt_default
        profile_btn.pack(side="right", anchor="ne")

        # tạo các button trong thanh tab bar
        self.empl_btn = ttk.Button(self.tab_bar_view, text="Nhân viên", compound='left', command=lambda: self.__action_tab(button_type=TabType.EMPLOYEE))
        self.empl_btn.grid(row=0, column=0, sticky='ns')
        self.__set_ui_default_emp_tab()

        ic_table = ImageTk.PhotoImage(Image.open("../assets/ic_table.png").resize(HomeView.size_icon_tab))
        self.table_btn = ttk.Button(self.tab_bar_view, text="Đặt bàn",
                                    compound='left',
                                    command=lambda: self.__action_tab(button_type=TabType.TABLE))
        self.table_btn.grid(row=0, column=1, sticky='ns')
        self.__set_ui_default_table_tab()

        self.bill_btn = ttk.Button(self.tab_bar_view, text="Hóa đơn",
                                   compound='left', command=lambda: self.__action_tab(button_type=TabType.BILL))
        self.bill_btn.grid(row=0, column=2, sticky='ns')
        self.__set_ui_default_bill_tab()

        self.ware_house_btn = ttk.Button(self.tab_bar_view, text="Nhà kho",
                                        compound='left', command=lambda: self.__action_tab(button_type=TabType.WARE_HOUSE))
        self.ware_house_btn.grid(row=0, column=3, sticky='ns')
        self.__set_ui_default_ware_house_tab()

        self.report_btn = ttk.Button(self.tab_bar_view, text="Báo cáo",
                                     compound='left', command=lambda: self.__action_tab(button_type=TabType.REPORT))
        self.report_btn.grid(row=0, column=4, sticky='ns')
        self.__set_ui_default_report_tab()

        self.logout_btn = ttk.Button(self.tab_bar_view, text="Đăng xuất",
                                     compound='left', command=lambda: self.__action_tab(button_type=TabType.LOGOUT))
        self.logout_btn.grid(row=0, column=5, sticky='ns')
        self.__set_ui_default_logout_tab()

        for i in range(len(self.tab_bar_view.winfo_children())):
            self.tab_bar_view.grid_columnconfigure(i, weight=1)


    def employee_page(self, main_fr):
        # add employee frame
        empl_page_fr = EmployeeView(main_fr)

    def table_page(self, main_fr):
        self.__root.style = ttk.Style()
        self.__root.style.theme_use("default")
        page = TableController(main_fr)

    def bill_page(self, main_fr):
        bill_fr = tk.Frame(main_fr, bg="green")
        bill_fr.pack(fill=tk.BOTH, expand=1)

    def warehouse_page(self, main_fr):
        warehouse_fr = tk.Frame(main_fr, bg="blue")
        warehouse_fr.pack(fill=tk.BOTH, expand=1)

    def report_page(self, main_fr):
        report_fr = tk.Frame(main_fr, bg="white")
        report_fr.pack(fill=tk.BOTH, expand=1)

    #Cập nhật ui tab đã chọn trước đó
    def __update_tab_clicked(self):
        if HomeView.button_type_clicked == TabType.EMPLOYEE:
            self.__set_ui_default_emp_tab()
        elif HomeView.button_type_clicked == TabType.TABLE:
            self.__set_ui_default_table_tab()
        elif HomeView.button_type_clicked == TabType.BILL:
            self.__set_ui_default_bill_tab()
        elif HomeView.button_type_clicked == TabType.WARE_HOUSE:
            self.__set_ui_default_ware_house_tab()
        elif HomeView.button_type_clicked == TabType.REPORT:
            self.__set_ui_default_report_tab()
        elif HomeView.button_type_clicked == TabType.LOGOUT:
            self.__set_ui_default_logout_tab()

    def __action_tab(self, button_type: TabType):
        self.__update_tab_clicked()
        HomeView.button_type_clicked = button_type
        # Hủy đi màn hinh load tab cũ
        for fr in self.__main_fr.winfo_children():
            fr.destroy()
            self.__root.update()

        if button_type == TabType.EMPLOYEE:
            ic_empl_click = ImageTk.PhotoImage(Image.open("../assets/ic_employees_click.png").resize(HomeView.size_icon_tab))
            self.empl_btn.config(style='Custom.CLiked.TButton', image=ic_empl_click)
            self.empl_btn.image = ic_empl_click
            self.employee_page(self.__main_fr)
        elif button_type == TabType.TABLE:
            ic_table = ImageTk.PhotoImage(Image.open("../assets/ic_table_white.png").resize(HomeView.size_icon_tab))
            self.table_btn.config(image=ic_table, style='Custom.CLiked.TButton')
            self.table_btn.image = ic_table
            self.table_page(self.__main_fr)
        elif button_type == TabType.BILL:
            ic_bill_click = ImageTk.PhotoImage(Image.open("../assets/ic_bill_click.png").resize(HomeView.size_icon_tab))
            self.bill_btn.config(style='Custom.CLiked.TButton', image=ic_bill_click)
            self.bill_btn.image = ic_bill_click
            self.bill_page(self.__main_fr)
        elif button_type == TabType.WARE_HOUSE:
            ic_ware_house_click = ImageTk.PhotoImage(Image.open("../assets/ic_house_click.png").resize(HomeView.size_icon_tab))
            self.ware_house_btn.config(style='Custom.CLiked.TButton', image=ic_ware_house_click)
            self.ware_house_btn.image = ic_ware_house_click
            self.warehouse_page(self.__main_fr)
        elif button_type == TabType.REPORT:
            ic_report_click = ImageTk.PhotoImage(Image.open("../assets/ic_chart_click.png").resize(HomeView.size_icon_tab))
            self.report_btn.config(style='Custom.CLiked.TButton', image=ic_report_click)
            self.report_btn.image = ic_report_click
            self.report_page(self.__main_fr)
        elif button_type == TabType.LOGOUT:
            ic_logout_click = ImageTk.PhotoImage(Image.open("../assets/ic_logout_click.png").resize(HomeView.size_icon_tab))
            self.logout_btn.config(style='Custom.CLiked.TButton', image=ic_logout_click)
            self.logout_btn.image = ic_logout_click

    def __set_ui_default_emp_tab(self):
        ic_emp_default = ImageTk.PhotoImage(Image.open("../assets/ic_employees_default.png").resize(HomeView.size_icon_tab))
        self.empl_btn.config(style='Custom.Normal.TButton', image=ic_emp_default)
        self.empl_btn.image = ic_emp_default

    def __set_ui_default_table_tab(self):
        ic_table_default = ImageTk.PhotoImage(Image.open("../assets/ic_table.png").resize(HomeView.size_icon_tab))
        self.table_btn.config(style='Custom.Normal.TButton', image=ic_table_default)
        self.table_btn.image = ic_table_default

    def __set_ui_default_bill_tab(self):
        ic_bill_default = ImageTk.PhotoImage(Image.open("../assets/ic_bill_default.png").resize(HomeView.size_icon_tab))
        self.bill_btn.config(style='Custom.Normal.TButton', image=ic_bill_default)
        self.bill_btn.image = ic_bill_default

    def __set_ui_default_ware_house_tab(self):
        ic_ware_house_default = ImageTk.PhotoImage(
            Image.open("../assets/ic_house_default.png").resize(HomeView.size_icon_tab))
        self.ware_house_btn.config(style='Custom.Normal.TButton', image=ic_ware_house_default)
        self.ware_house_btn.image = ic_ware_house_default

    def __set_ui_default_report_tab(self):
        ic_report_default = ImageTk.PhotoImage(
            Image.open("../assets/ic_chart_default.png").resize(HomeView.size_icon_tab))
        self.report_btn.config(style='Custom.Normal.TButton', image=ic_report_default)
        self.report_btn.image = ic_report_default

    def __set_ui_default_logout_tab(self):
        ic_logout_default = ImageTk.PhotoImage(
            Image.open("../assets/ic_logout_default.png").resize(HomeView.size_icon_tab))
        self.logout_btn.config(style='Custom.Normal.TButton', image=ic_logout_default)
        self.logout_btn.image = ic_logout_default


