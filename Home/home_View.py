from tkinter import ttk
from PIL import Image
from Bill.bill_controller import BillController
from Report.report_view import ReportView
from Table_Order.table_controller import TableController
from WareHouse.ware_house_controller import WareHouseController
from admin.logout.logout_controller import LogoutController
from employee_view import EmployeeView
from customtkinter import *
from share.common_config import TabType
import os


class HomeView():
    button_type_clicked = TabType.EMPLOYEE
    size_icon_tab = (35, 35)
    hover_color_tab = "LightSkyBlue"
    fg_color_tab_click = "DodgerBlue1"
    fg_color_tab_normal = "#FFFFFF"
    radius_tab = 5
    def __init__(self, window):
        self.__root = window
        # Tạo frame thanh tab bar
        self.__generate_ui_header(window)

        # Tạo một frame chính để chuyển đổi nhiều page
        self.__main_fr = ttk.Frame(window)
        self.__main_fr.pack(fill="both", expand=1)

        # Mặc định chọn tab 1: Hiển thị page nhân viên
        self.empl_btn.configure(fg_color=HomeView.fg_color_tab_click, text_color="white")
        self.employee_page(self.__main_fr)

    def __generate_ui_header(self, window):
        header_view = ttk.Frame(window, borderwidth=5)
        header_view.pack(fill="both", expand=0)
        self.tab_bar_view = ttk.Frame(header_view)
        self.tab_bar_view.pack(side="left")
        avt_default = self.get_image_file("../assets/avatar_default_man.png")

        profile_btn = CTkButton(header_view, text="Admin director", image=avt_default, corner_radius=0,
                                bg_color="white", fg_color="black")
        profile_btn.pack(side="right", anchor="ne")

        # Tạo các button trong thanh tab bar
        font_tab = CTkFont("TkDefaultFont", 16, 'bold')
        ipadx_tab_button = 10
        self.empl_btn = CTkButton(self.tab_bar_view, text="Nhân viên", compound='top',
                                  corner_radius=HomeView.radius_tab,
                                  fg_color=HomeView.fg_color_tab_click,
                                  font=font_tab,
                                  hover_color=HomeView.hover_color_tab,
                                  border_width=1,
                                  border_color="#0033CC",
                                  command=lambda: self.__action_tab(button_type=TabType.EMPLOYEE))
        self.empl_btn.grid(row=0, column=0, sticky='ns', ipady=3, ipadx=ipadx_tab_button)
        self.__set_ui_default_emp_tab()

        # Table tab
        self.table_btn = CTkButton(self.tab_bar_view, text="Đặt bàn",
                                   corner_radius=HomeView.radius_tab,
                                   fg_color=HomeView.fg_color_tab_normal,
                                   font=font_tab,
                                   hover_color=HomeView.hover_color_tab,
                                   border_width=1,
                                   border_color="#0033CC",
                                   compound='top',
                                   command=lambda: self.__action_tab(button_type=TabType.TABLE))

        self.table_btn.grid(row=0, column=1, sticky='ns', ipady=3, ipadx=ipadx_tab_button)
        self.__set_ui_default_table_tab()

        # Invoice tab
        self.bill_btn = CTkButton(self.tab_bar_view, text="Hóa đơn",
                                  compound='top',
                                  corner_radius=HomeView.radius_tab,
                                  fg_color=HomeView.fg_color_tab_normal,
                                  font=font_tab,
                                  hover_color=HomeView.hover_color_tab,
                                  border_width=1,
                                  border_color="#0033CC",
                                  command=lambda: self.__action_tab(button_type=TabType.BILL))
        self.bill_btn.grid(row=0, column=2, sticky='ns', ipady=3, ipadx=ipadx_tab_button)
        self.__set_ui_default_bill_tab()

        # Warehouse tab
        self.ware_house_btn = CTkButton(self.tab_bar_view, text="Nhà kho",
                                        corner_radius=HomeView.radius_tab,
                                        fg_color=HomeView.fg_color_tab_normal,
                                        font=font_tab,
                                        hover_color=HomeView.hover_color_tab,
                                        border_width=1,
                                        border_color="#0033CC",
                                        compound="top",
                                        command=lambda: self.__action_tab(button_type=TabType.WARE_HOUSE))
        self.ware_house_btn.grid(row=0, column=3, sticky='ns', ipady=3, ipadx=ipadx_tab_button)
        self.__set_ui_default_ware_house_tab()

        # Report button
        self.report_btn = CTkButton(self.tab_bar_view, text="Báo cáo",
                                    corner_radius=HomeView.radius_tab,
                                    fg_color=HomeView.fg_color_tab_normal,
                                    font=font_tab,
                                    hover_color=HomeView.hover_color_tab,
                                    border_width=1,
                                    border_color="#0033CC",
                                    compound='top', command=lambda: self.__action_tab(button_type=TabType.REPORT))
        self.report_btn.grid(row=0, column=4, sticky='ns', ipady=3, ipadx=ipadx_tab_button)
        self.__set_ui_default_report_tab()

        # Logout tab
        self.logout_btn = CTkButton(self.tab_bar_view, text="Đăng xuất",
                                    corner_radius=HomeView.radius_tab,
                                    fg_color=HomeView.fg_color_tab_normal,
                                    font=font_tab,
                                    hover_color=HomeView.hover_color_tab,
                                    border_width=1,
                                    border_color="#0033CC",
                                    compound='top', command=lambda: self.__action_tab(button_type=TabType.LOGOUT))
        self.logout_btn.grid(row=0, column=5, sticky='ns', ipady=3, ipadx=ipadx_tab_button)
        self.__set_ui_default_logout_tab()

        for i in range(len(self.tab_bar_view.winfo_children())):
            self.tab_bar_view.grid_columnconfigure(i, weight=1)

    def employee_page(self, main_fr):
        # add employee fram
        self.__root.style = ttk.Style()
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
            self.empl_btn.configure(fg_color=HomeView.fg_color_tab_click, text_color="white")
            self.employee_page(self.__main_fr)
        elif button_type == TabType.TABLE:
            self.table_btn.configure(fg_color=HomeView.fg_color_tab_click, text_color="white")
            self.table_page(self.__main_fr)
        elif button_type == TabType.BILL:
            self.bill_btn.configure(text_color="white", fg_color=HomeView.fg_color_tab_click)
            self.bill_page(self.__main_fr)
        elif button_type == TabType.WARE_HOUSE:
            self.ware_house_btn.configure(text_color="white", fg_color=HomeView.fg_color_tab_click)
            self.warehouse_page(self.__main_fr)
        elif button_type == TabType.REPORT:
            self.report_btn.configure(text_color="white", fg_color=HomeView.fg_color_tab_click)
            self.report_page(self.__main_fr)
        elif button_type == TabType.LOGOUT:
            self.logout_btn.configure(text_color="white", fg_color=HomeView.fg_color_tab_click)
            self.on_logout_click()

    def __set_ui_default_emp_tab(self):
        ic_emp_default = CTkImage(Image.open("../assets/ic_tab_employees.png"), size=HomeView.size_icon_tab)
        self.empl_btn.configure(image=ic_emp_default, text_color="black", fg_color=HomeView.fg_color_tab_normal)

    def __set_ui_default_table_tab(self):
        ic_table_default = CTkImage(Image.open("../assets/restaurant.ico"), size=HomeView.size_icon_tab)
        self.table_btn.configure(text_color="black", fg_color=HomeView.fg_color_tab_normal, image=ic_table_default)

    def __set_ui_default_bill_tab(self):
        ic_bill_default = CTkImage(Image.open("../assets/invoice.png"), size=HomeView.size_icon_tab)
        self.bill_btn.configure(text_color="black", fg_color=HomeView.fg_color_tab_normal, image=ic_bill_default)
        self.bill_btn.image = ic_bill_default

    def __set_ui_default_ware_house_tab(self):
        ic_ware_house_default = CTkImage(Image.open("../assets/delivery.png"), size=HomeView.size_icon_tab)
        self.ware_house_btn.configure(text_color="black", fg_color=HomeView.fg_color_tab_normal, image=ic_ware_house_default)

    def __set_ui_default_report_tab(self):
        ic_report_default = CTkImage(Image.open("../assets/pie-chart.png"), size=HomeView.size_icon_tab)
        self.report_btn.configure(text_color="black", fg_color=HomeView.fg_color_tab_normal, image=ic_report_default)

    def __set_ui_default_logout_tab(self):
        ic_logout_default = CTkImage(Image.open("../assets/logout.png"), size=HomeView.size_icon_tab)
        self.logout_btn.configure(text_color="black", fg_color=HomeView.fg_color_tab_normal, image=ic_logout_default)
    

    def get_image_file(self, path_file:str):
        try:
            if path_file == "": return
            path = ""
            if os.path.exists(path_file):
                path = path_file
            else:
                path = f"../{path_file}"
            if os.path.exists(path):
                return CTkImage(Image.open(path).resize(HomeView.size_icon_tab))
        except Exception as ex:
            print(ex)
