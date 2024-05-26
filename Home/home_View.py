from tkinter import ttk
from PIL import Image
from Bill.bill_controller import BillController
from Report.report_view import ReportView
from Table_Order.table_controller import TableController
from WareHouse.ware_house_controller import WareHouseController
from WareHouse.ware_house_view import WareHouseView
from admin.logout.logout_controller import LogoutController
from employee_view import EmployeeView
from customtkinter import *
from share.common_config import TabType


class HomeView:
    button_type_clicked = TabType.EMPLOYEE
    size_icon_tab = (28, 28)

    def __init__(self, window):
        self.__root = window
        # Tạo frame thanh tab bar
        self.__generate_ui_header(window)

        # Tạo một frame chính để chuyển đổi nhiều page
        self.__main_fr = ttk.Frame(window)
        self.__main_fr.pack(fill="both", expand=1)

        # Mặc định chọn tab 1: Hiển thị page nhân viên
        ic_empl_click = CTkImage(Image.open("../assets/ic_employees_click.png").resize(HomeView.size_icon_tab))
        self.empl_btn.configure(image=ic_empl_click, fg_color="blue", text_color="white")
        self.employee_page(self.__main_fr)

    def __generate_ui_header(self, window):
        header_view = ttk.Frame(window, borderwidth=5)
        header_view.pack(fill="both", expand=0)
        self.tab_bar_view = ttk.Frame(header_view)
        self.tab_bar_view.pack(side="left")
        avt_default = CTkImage(Image.open("../assets/avatar_default_man.png").resize((35, 35)))

        profile_btn = CTkButton(header_view, text="Admin director", image=avt_default, corner_radius=0,
                                bg_color="white", fg_color="black")
        profile_btn.pack(side="right", anchor="ne")

        # Tạo các button trong thanh tab bar
        self.empl_btn = CTkButton(self.tab_bar_view, text="Nhân viên", compound='left', corner_radius=0,
                                  fg_color="white",
                                  command=lambda: self.__action_tab(button_type=TabType.EMPLOYEE))
        self.empl_btn.grid(row=0, column=0, sticky='ns')
        self.__set_ui_default_emp_tab()

        # Table tab
        self.table_btn = CTkButton(self.tab_bar_view, text="Đặt bàn",
                                   compound='left', corner_radius=0,
                                   command=lambda: self.__action_tab(button_type=TabType.TABLE))

        self.table_btn.grid(row=0, column=1, sticky='ns')
        self.__set_ui_default_table_tab()

        # Invoice tab
        self.bill_btn = CTkButton(self.tab_bar_view, text="Hóa đơn", corner_radius=0, compound='left',
                                  command=lambda: self.__action_tab(button_type=TabType.BILL))
        self.bill_btn.grid(row=0, column=2, sticky='ns')
        self.__set_ui_default_bill_tab()

        # Warehouse tab
        self.ware_house_btn = CTkButton(self.tab_bar_view, text="Nhà kho", corner_radius=0,
                                        compound='left',
                                        command=lambda: self.__action_tab(button_type=TabType.WARE_HOUSE))
        self.ware_house_btn.grid(row=0, column=3, sticky='ns')
        self.__set_ui_default_ware_house_tab()

        # Report button
        self.report_btn = CTkButton(self.tab_bar_view, text="Báo cáo", corner_radius=0,
                                    compound='left', command=lambda: self.__action_tab(button_type=TabType.REPORT))
        self.report_btn.grid(row=0, column=4, sticky='ns')
        self.__set_ui_default_report_tab()

        # Logout tab
        self.logout_btn = CTkButton(self.tab_bar_view, text="Đăng xuất", corner_radius=0,
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
        page = BillController(main_fr)

    def warehouse_page(self, main_fr):
        warehouse_fr = WareHouseController(main_fr)

    def report_page(self, main_fr):
        report_fr = ReportView(main_fr)

    def on_logout_click(self):
        logout_controller = LogoutController()
        logout_controller.logout()

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
            ic_empl_click = CTkImage(Image.open("../assets/ic_employees_click.png").resize(HomeView.size_icon_tab))
            self.empl_btn.configure(image=ic_empl_click, fg_color="blue", text_color="white")
            self.employee_page(self.__main_fr)
        elif button_type == TabType.TABLE:
            ic_table = CTkImage(Image.open("../assets/ic_table_white.png").resize(HomeView.size_icon_tab))
            self.table_btn.configure(image=ic_table, fg_color="blue", text_color="white")
            self.table_page(self.__main_fr)
        elif button_type == TabType.BILL:
            ic_bill_click = CTkImage(Image.open("../assets/ic_bill_click.png").resize(HomeView.size_icon_tab))
            self.bill_btn.configure(fg_color="blue", text_color="white", image=ic_bill_click)
            self.bill_page(self.__main_fr)
        elif button_type == TabType.WARE_HOUSE:
            ic_ware_house_click = CTkImage(
                Image.open("../assets/ic_house_click.png").resize(HomeView.size_icon_tab))
            self.ware_house_btn.configure(fg_color="blue", text_color="white", image=ic_ware_house_click)
            self.ware_house_btn.image = ic_ware_house_click
            self.warehouse_page(self.__main_fr)
        elif button_type == TabType.REPORT:
            ic_report_click = CTkImage(Image.open("../assets/ic_chart_click.png").resize(HomeView.size_icon_tab))
            self.report_btn.configure(fg_color="blue", text_color="white", image=ic_report_click)
            self.report_btn.image = ic_report_click
            self.report_page(self.__main_fr)
        elif button_type == TabType.LOGOUT:
            ic_logout_click = CTkImage(Image.open("../assets/ic_logout_click.png").resize(HomeView.size_icon_tab))
            self.logout_btn.configure(fg_color="blue", text_color="white", image=ic_logout_click)
            self.logout_btn.image = ic_logout_click
            self.on_logout_click()

    def __set_ui_default_emp_tab(self):
        ic_emp_default = CTkImage(Image.open("../assets/ic_employees_default.png").resize(HomeView.size_icon_tab))
        self.empl_btn.configure(image=ic_emp_default, text_color="black", fg_color="white")

    def __set_ui_default_table_tab(self):
        ic_table_default = CTkImage(Image.open("../assets/ic_table.png").resize(HomeView.size_icon_tab))
        self.table_btn.configure(text_color="black", fg_color="white", image=ic_table_default)

    def __set_ui_default_bill_tab(self):
        ic_bill_default = CTkImage(Image.open("../assets/ic_bill_default.png").resize(HomeView.size_icon_tab))
        self.bill_btn.configure(text_color="black", fg_color="white", image=ic_bill_default)
        self.bill_btn.image = ic_bill_default

    def __set_ui_default_ware_house_tab(self):
        ic_ware_house_default = CTkImage(Image.open("../assets/ic_house_default.png").resize(HomeView.size_icon_tab))
        self.ware_house_btn.configure(text_color="black", fg_color="white", image=ic_ware_house_default)

    def __set_ui_default_report_tab(self):
        ic_report_default = CTkImage(Image.open("../assets/ic_chart_default.png").resize(HomeView.size_icon_tab))
        self.report_btn.configure(text_color="black", fg_color="white", image=ic_report_default)

    def __set_ui_default_logout_tab(self):
        ic_logout_default = CTkImage(Image.open("../assets/ic_logout_default.png").resize(HomeView.size_icon_tab))
        self.logout_btn.configure(text_color="black", fg_color="white", image=ic_logout_default)
