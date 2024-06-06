import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
from bill.bill_controller import BillController
# from bill.bill_controller import BillController
from home.SlidePanel import SlidePanel
from logout.logout_controller import LogoutController
from report.report_controller import ReportController
from table_order.table_controller import TableController
from warehouse.ware_house_controller import WareHouseController
from employee.employee_view import EmployeeView
from logout.logout_controller import LogoutController
from share.common_config import TabType, UserType
from share.utils import Utils
import tkinter.messagebox as tkMsgBox
from change_password.change_password_view import ChangePasswordView


class HomeView:
    button_type_clicked = TabType.EMPLOYEE
    size_icon_tab = (35, 35)
    hover_color_tab = "LightSkyBlue"
    fg_color_tab_click = "DodgerBlue1"
    fg_color_tab_normal = "#FFFFFF"
    radius_tab = 5

    def __init__(self, window, controller):
        self.__root = window
        self.__controller = controller
        self._user_type = Utils.user_profile["type"]
        # style = ttk.Style()
        # style.theme_use("default")
        # Utils.set_appearance_mode(ctk)
        self.home_fr = ctk.CTkFrame(master=window, fg_color="white", corner_radius=0)
        self.home_fr.pack(fill=tk.BOTH, expand=1)
        # Tạo UI thanh tab bar
        self.__generate_ui_header(window=self.home_fr)

        # Tạo một frame chính để chuyển đổi nhiều page
        self.__main_fr = ctk.CTkFrame(master=self.home_fr, fg_color="white")
        self.__main_fr.pack(fill="both", expand=1)

        # Mặc định chọn tab 1: Hiển thị nhân viên page
        if self._user_type == UserType.ADMIN.value:
            HomeView.button_type_clicked = TabType.EMPLOYEE
            self.employee_page(self.__main_fr)
            self.empl_btn.configure(fg_color=HomeView.fg_color_tab_click, text_color="white")
            self.table_btn.configure(text="Bàn")
        else:
            HomeView.button_type_clicked = TabType.TABLE
            self.__main_fr.update_idletasks()
            self.table_page(self.__main_fr)
            self.table_btn.configure(fg_color=HomeView.fg_color_tab_click, text_color="white")

    def __generate_ui_header(self, window):
        # animated widget
        animated_panel = SlidePanel(self.__root, 1, 0.866)
        animated_panel.configure(corner_radius=0, border_color="gray", border_width=1, fg_color="white")
        ic_change_password = ctk.CTkImage(Image.open("../assets/padlock.png"), size=(25, 25))
        change_password_btn = ctk.CTkButton(animated_panel, text='Đổi mật khẩu',
                                            corner_radius=0, fg_color="white", text_color="black",
                                            hover_color=HomeView.hover_color_tab,
                                            image=ic_change_password,
                                            font=ctk.CTkFont("Roboto", 16),
                                            command=lambda: self.on_change_pass())
        change_password_btn.pack(expand=False, fill=tk.X, pady=(10, 0), padx=2)
        ic_logout_default = ctk.CTkImage(Image.open("../assets/logout.png"), size=(25, 25))
        logout_btn = ctk.CTkButton(animated_panel, text='Logout', corner_radius=0, fg_color="white",
                                   hover_color=HomeView.hover_color_tab,
                                   font=ctk.CTkFont("Roboto", 16),
                                   image=ic_logout_default, compound=tk.LEFT, text_color="black",
                                   command=lambda: self.on_logout_click())
        logout_btn.pack(expand=False, fill=tk.X, pady=10, padx=2)

        header_view = ctk.CTkFrame(window,corner_radius=0, fg_color="white")
        header_view.pack(fill=tk.X, expand=0, padx=(3, 0))
        font_tab = ctk.CTkFont("TkDefaultFont", 16, 'bold')
        ipadx_tab_button = 10
        self.tab_bar_view = ctk.CTkFrame(header_view)
        self.tab_bar_view.pack(side="left")

        avt_default = ctk.CTkImage(Image.open("../assets/avatar_default_man.png"), size=(30, 30))
        profile_btn = ctk.CTkButton(header_view, text=Utils.user_profile["user_name"],
                                    image=avt_default, corner_radius=0,
                                    width=200,
                                    font=font_tab,
                                    text_color="#000080",
                                    bg_color="white",
                                    fg_color="white",
                                    compound=tk.RIGHT,
                                    hover_color=HomeView.hover_color_tab,
                                    command=lambda: animated_panel.animate())
        profile_btn.pack(fill=tk.Y, side="right", anchor="ne", pady=(0, 6))

        # Tạo các button trong thanh tab bar
        if self._user_type == UserType.ADMIN.value:
            self.empl_btn = ctk.CTkButton(self.tab_bar_view, text="Nhân viên", compound='top',
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
        self.table_btn = ctk.CTkButton(self.tab_bar_view, text="Đặt bàn",
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
        self.bill_btn = ctk.CTkButton(self.tab_bar_view, text="Hóa đơn",
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
        self.ware_house_btn = ctk.CTkButton(self.tab_bar_view, text="Nhà kho",
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
        if self._user_type == UserType.ADMIN.value:
            self.report_btn = ctk.CTkButton(self.tab_bar_view, text="Báo cáo",
                                            corner_radius=HomeView.radius_tab,
                                            fg_color=HomeView.fg_color_tab_normal,
                                            font=font_tab,
                                            hover_color=HomeView.hover_color_tab,
                                            border_width=1,
                                            border_color="#0033CC",
                                            compound='top', command=lambda: self.__action_tab(button_type=TabType.REPORT))
            self.report_btn.grid(row=0, column=4, sticky='ns', ipady=3, ipadx=ipadx_tab_button)
            self.__set_ui_default_report_tab()

        for i in range(len(self.tab_bar_view.winfo_children())):
            self.tab_bar_view.grid_columnconfigure(i, weight=1)

    def employee_page(self, main_fr):
        # add employee frame
        empl_page_fr = EmployeeView(main_fr)

    def table_page(self, main_fr):
        page = TableController(main_fr)

    def bill_page(self, main_fr):
        page = BillController(main_fr)

    def warehouse_page(self, main_fr):
        warehouse_fr = WareHouseController(main_fr)

    def report_page(self, main_fr):
        report_p = ReportController(root=main_fr)

    def on_logout_click(self):
        response = tkMsgBox.askyesno("Thông báo", "Bạn có muốn đăng xuất?")
        if response:
            self.__main_fr.destroy()
            self.home_fr.destroy()

            # Recreate frame
            self.home_fr = ctk.CTkFrame(master=self.__root, fg_color="white", corner_radius=0)
            self.home_fr.pack(fill=tk.BOTH, expand=1)

            self.__main_fr = ctk.CTkFrame(master=self.home_fr, fg_color="white")
            self.__main_fr.pack(fill="both", expand=True, side=tk.LEFT)

            logout_controller = LogoutController()
            logout_controller.logout(self.__main_fr)

    def on_change_pass(self):
        # User can change own password
        frame = ctk.CTkFrame(self.__main_fr)
        change_password = ChangePasswordView()
        change_password.init_change_password_popup(frame)

    # Cập nhật ui tab đã chọn trước đó
    def __update_tab_clicked(self):
        if self._user_type == UserType.ADMIN.value:
            if HomeView.button_type_clicked == TabType.EMPLOYEE:
                self.__set_ui_default_emp_tab()
            elif HomeView.button_type_clicked == TabType.REPORT:
                self.__set_ui_default_report_tab()
        if HomeView.button_type_clicked == TabType.TABLE:
            self.__set_ui_default_table_tab()
        elif HomeView.button_type_clicked == TabType.BILL:
            self.__set_ui_default_bill_tab()
        elif HomeView.button_type_clicked == TabType.WARE_HOUSE:
            self.__set_ui_default_ware_house_tab()


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

    def __set_ui_default_emp_tab(self):
        ic_emp_default = ctk.CTkImage(Image.open("../assets/ic_tab_employees.png"), size=HomeView.size_icon_tab)
        self.empl_btn.configure(image=ic_emp_default, text_color="black", fg_color=HomeView.fg_color_tab_normal)

    def __set_ui_default_table_tab(self):
        ic_table_default = ctk.CTkImage(Image.open("../assets/restaurant.ico"), size=HomeView.size_icon_tab)
        self.table_btn.configure(text_color="black", fg_color=HomeView.fg_color_tab_normal, image=ic_table_default)

    def __set_ui_default_bill_tab(self):
        ic_bill_default = ctk.CTkImage(Image.open("../assets/invoice.png"), size=HomeView.size_icon_tab)
        self.bill_btn.configure(text_color="black", fg_color=HomeView.fg_color_tab_normal, image=ic_bill_default)
        self.bill_btn.image = ic_bill_default

    def __set_ui_default_ware_house_tab(self):
        ic_ware_house_default = ctk.CTkImage(Image.open("../assets/delivery.png"), size=HomeView.size_icon_tab)
        self.ware_house_btn.configure(text_color="black", fg_color=HomeView.fg_color_tab_normal,
                                      image=ic_ware_house_default)

    def __set_ui_default_report_tab(self):
        ic_report_default = ctk.CTkImage(Image.open("../assets/pie-chart.png"), size=HomeView.size_icon_tab)
        self.report_btn.configure(text_color="black", fg_color=HomeView.fg_color_tab_normal, image=ic_report_default)