import tkinter
import customtkinter
from functools import partial
import customtkinter as ctk
from PIL import Image
from employee_view import EmployeeView
from share.common_config import Tab
from share.utils import Utils
DARK_MODE = "light"
customtkinter.set_appearance_mode(DARK_MODE)
customtkinter.set_default_color_theme("blue")


class TabControls(customtkinter.CTk):
    frames = {}
    current_tab = None

    def __init__(self, parent):
        super().__init__()
        self.__parent = parent
        self.__top_panel = None
        self.__body = ctk.CTkFrame(parent)
        self.__cur_tab_id = 0
        self.init_view(parent)

    def init_view(self, parent):

        # Contain all information of page
        main_container = customtkinter.CTkFrame(master=parent, corner_radius=8)
        main_container.pack(fill=tkinter.BOTH, expand=True, padx=8, pady=8)

        # Top panel: contain all tab of application
        self.__top_panel = customtkinter.CTkFrame(main_container, height=300, corner_radius=8)
        self.__top_panel.pack(side=tkinter.TOP, fill=tkinter.X, expand=False, padx=3, pady=3)

        # Body: display all content of each tab when user click on
        self.__body = customtkinter.CTkFrame(main_container, corner_radius=8, fg_color="#212121")
        self.__body.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        self.__body.configure(border_width=1)
        self.__body.configure(border_color="#323232")

        # Create tab and body for UI
        self.create_tab_and_body(self.__top_panel, Tab.EMPLOYEE)
        self.create_tab_and_body(self.__top_panel, Tab.TABLE)
        self.create_tab_and_body(self.__top_panel, Tab.INVOICE)
        self.create_tab_and_body(self.__top_panel, Tab.WARE_HOUSE)
        self.create_tab_and_body(self.__top_panel, Tab.REPORT)
        self.create_tab_and_body(self.__top_panel, Tab.LOG_OUT)

    def create_tab_selector(self, parent, tab_id: Tab):
        if tab_id == Tab.EMPLOYEE:
            self.create_tab_btn("../../assets/officer.png", "Nhân viên", tab_id)
        elif tab_id == Tab.TABLE:
            self.create_tab_btn("../../assets/around-table.png", "Bàn", tab_id)
        elif tab_id == Tab.INVOICE:
            self.create_tab_btn("../../assets/shopping-bag.png", "Hoá đơn", tab_id)
        elif tab_id == Tab.WARE_HOUSE:
            self.create_tab_btn("../../assets/warehouse.png", "Kho", tab_id)
        elif tab_id == Tab.REPORT:
            self.create_tab_btn("../../assets/calendar.png", "Báo cáo", tab_id)
        elif tab_id == Tab.LOG_OUT:
            self.create_tab_btn("../../assets/logout.png", "Đăng xuất", tab_id)

    def create_tab_btn(self, logo_path, btn_name, tab_id: Tab):
        try:
            img = ctk.CTkImage(light_image=Image.open(logo_path), dark_image=Image.open(logo_path), size=(30, 30))
            tab = customtkinter.CTkButton(self.__top_panel, fg_color=Utils.WHITE)
            tab.configure(text_color=Utils.BLUE)
            tab.configure(width=200)
            tab.configure(text=btn_name)
            tab.configure(image=img)
            tab.configure(command=lambda: self.toggle_body_by_id(tab_id))
            tab.pack(side="left", padx=3, expand=False)
        except IOError as err:
            print(err)

    def create_body(self, tab_id):
        TabControls.frames[tab_id] = customtkinter.CTkFrame(master=self.__body)
        TabControls.frames[tab_id].configure(corner_radius=8)
        TabControls.frames[tab_id].configure(border_width=2)
        TabControls.frames[tab_id].configure(border_color="#323232")
        TabControls.frames[tab_id].pady = 8

        if tab_id == Tab.EMPLOYEE:
            TabControls.frames[tab_id] = customtkinter.CTkFrame(master=self.__body)
            employee_page = EmployeeView(self.__body)
        elif tab_id == Tab.TABLE:
            TabControls.frames[tab_id] = customtkinter.CTkFrame(master=self.__body)
            lbl = ctk.CTkLabel(TabControls.frames[tab_id], text="Table", font=('', 50, 'bold'), justify='center',
                               text_color=Utils.BLUE, pady=50)
            lbl.pack(side='left')
        elif tab_id == Tab.INVOICE:
            TabControls.frames[tab_id] = customtkinter.CTkFrame(master=self.__body)
            lbl = ctk.CTkLabel(TabControls.frames[tab_id], text="Invoice", font=('', 50, 'bold'), justify='center',
                               text_color=Utils.BLUE, pady=50)
            lbl.pack(side='left')
        elif tab_id == Tab.REPORT:
            TabControls.frames[tab_id] = customtkinter.CTkFrame(master=self.__body)
            lbl = ctk.CTkLabel(TabControls.frames[tab_id], text="Report", font=('', 50, 'bold'), justify='center',
                               text_color=Utils.BLUE, pady=50)
            lbl.pack(side='left')
        elif tab_id == Tab.WARE_HOUSE:
            TabControls.frames[tab_id] = customtkinter.CTkFrame(master=self.__body)
            lbl = ctk.CTkLabel(TabControls.frames[tab_id], text="WareHouse", font=('', 50, 'bold'), justify='center',
                               text_color=Utils.BLUE, pady=50)
            lbl.pack(side='left')
        elif tab_id == Tab.LOG_OUT:
            TabControls.frames[tab_id] = customtkinter.CTkFrame(master=self.__body)
            lbl = ctk.CTkLabel(TabControls.frames[tab_id], text="Log out", font=('', 50, 'bold'), justify='center',
                               text_color=Utils.BLUE, pady=50)
            lbl.pack(side='left')

    def toggle_body_by_id(self, tab_id):
        if TabControls.frames[tab_id] is not None:
            if TabControls.current_tab is TabControls.frames[tab_id]:
                TabControls.current_tab.pack_forget()
                TabControls.current_tab = None
            elif TabControls.current_tab is not None:
                TabControls.current_tab.pack_forget()
                TabControls.current_tab = TabControls.frames[tab_id]
                TabControls.current_tab.pack(in_=self.__body, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
            else:
                TabControls.current_tab = TabControls.frames[tab_id]
                TabControls.current_tab.pack(in_=self.__body, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        self.__cur_tab_id = tab_id

    def create_tab_and_body(self, parent, tab_id):
        self.create_tab_selector(parent, tab_id)
        self.create_body(tab_id)