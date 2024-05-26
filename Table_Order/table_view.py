import math
import tkinter as tk
from enum import Enum
from tkinter import ttk

import customtkinter
from PIL import Image, ImageTk

from Table_Order.table_model import TableType, Table
from share.CustomMenu import CustomMenu
from share.common_config import Action, UserType
from customtkinter import *
from functools import partial

class StatusTable(Enum):
    DISABLED = "Đã đặt"
    AVAILABLE = "Trống"
class TableView:
    def __init__(self, window, controller, tables, user_type):
        self.__controller = controller
        self.__user_type = user_type
        self.table_num_value = tk.StringVar()
        self.seat_num_value = tk.StringVar()
        self.status_value = tk.StringVar()
        self.__table_selected = Table()
        self.__screen_width = window.winfo_width()
        self.__screen_height = window.winfo_height()

        self.grid_frame = CTkFrame(window)
        self.grid_frame.pack(fill="both", expand=True)

        # Tạo thanh cuộn ngang
        self.horizontal_scrollbar = CTkScrollbar(self.grid_frame, orientation="horizontal")
        self.horizontal_scrollbar.pack(side="bottom", fill="x")

        # Tạo thanh cuộn dọc
        self.vertical_scrollbar = CTkScrollbar(self.grid_frame, orientation="vertical")
        self.vertical_scrollbar.pack(side="right", fill="y")

        # Tạo một canvas để chứa lưới
        self.canvas = CTkCanvas(self.grid_frame, xscrollcommand=self.horizontal_scrollbar.set,
                                yscrollcommand=self.vertical_scrollbar.set)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # Kết nối thanh cuộn với canvas
        self.horizontal_scrollbar.configure(command=self.canvas.xview)
        self.vertical_scrollbar.configure(command=self.canvas.yview)

        # Tạo một frame con để chứa bàn
        self.grid_content = CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.grid_content, anchor="nw")

        # Thêm ds bàn vào grid content
        self._add_content(window, self.__controller.tables)

        # Đặt sự kiện để cập nhật kích thước của canvas
        self.grid_content.bind("<Configure>", self.on_frame_configure)

        self.create_menu_option_right(window)




    def _add_content(self, window, tables):
        """Thêm nội dung vào Frame (trong trường hợp này là một grid)"""
        num_columns = 6
        column_width = self.__screen_width // 8
        row_height = self.__screen_height // 8
        image_size = 180
        num_rows = math.ceil(len(tables) / num_columns)
        for i in range(num_rows):
            for j in range(num_columns):
                index = i * num_columns + j
                if index < len(tables):
                    print(tables[index])
                    num_table = tables[index].tableNum
                    self.grid_content.grid_columnconfigure(j, weight=1)
                    img_table = ImageTk.PhotoImage(Image.open("../../assets/ic_table_visible.png").resize(
                        (image_size, image_size)))
                    btn = CTkButton(self.grid_content, text=num_table, image=img_table, anchor="c", compound="bottom",
                                    corner_radius=0, fg_color="white", text_color="blue",
                                    font=CTkFont("Roboto", 24, 'bold'),
                                    command=lambda t=tables[index]: self.selected_table(window, t))

                    btn.configure(image=img_table)
                    btn.bind("<Button-2>", lambda e, t=tables[index]: self.__show_context_popup(event=e, tableSelected=t))
                    btn.grid(row=i, column=j, sticky="nsew", padx=5, pady=5, ipadx=column_width // 4, ipady=row_height // 4)

    def update_data_table(self):
        pass

    def selected_table(self, window, table):
        if self.__user_type == UserType.ADMIN:
            if table.table_type == TableType.Add:
                self.create_ui_toplevel(window, Action.ADD)
                print("add table")
        else:
            # order
            print("selected table")
            pass

    def on_frame_configure(self, event):
        # Cập nhật kích thước của canvas khi nội dung thay đổi
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def create_ui_toplevel(self, window, action_type):
        customtkinter.set_appearance_mode("light")
        self.toplevel = CTkToplevel(window)
        self.toplevel.resizable(True, False)
        self.toplevel.geometry("290x250")
        validation = window.register(self.validate_input)
        table_popup_frame = CTkFrame(self.toplevel)
        lb_table_num = CTkLabel(table_popup_frame, text="Số bàn")
        lb_table_num.place(x=10, y=20)
        self.entry_table_num = CTkEntry(table_popup_frame, textvariable=self.table_num_value, validate="key")
        self.entry_table_num.place(x=80, y=20)

        lb_seat_num = CTkLabel(table_popup_frame, text="Số ghế")
        lb_seat_num.place(x=10, y=60)
        self.entry_seat_num = CTkEntry(table_popup_frame, textvariable=self.seat_num_value, validate="key",
                                       validatecommand=(validation, '%P'))
        self.entry_seat_num.place(x=80, y=60)

        lb_table_status = CTkLabel(table_popup_frame, text="Trạng thái")
        lb_table_status.place(x=10, y=100)
        self.status_combox = CTkComboBox(table_popup_frame, values=[StatusTable.AVAILABLE.value, StatusTable.DISABLED.value], state="readonly")
        self.status_combox.place(x=80, y=100)
        self.lb_validate_table_info = CTkLabel(table_popup_frame, text="", text_color="red")
        self.lb_validate_table_info.place(x=60, y=140)

        btn_save = CTkButton(table_popup_frame, text="Lưu", command=lambda: self.click_button_add_or_edit_popup(window, action_type))
        btn_save.pack(fill=tk.Y, expand=0, side="bottom", pady=40)
        if action_type == Action.ADD:
            self.table_num_value.set("")
            self.seat_num_value.set("")
            self.toplevel.title("Thêm bàn mới")
            self.status_combox.set(StatusTable.AVAILABLE.value)
            btn_save.configure(text="Lưu")
        else:
            print(f"{self.__table_selected.tableNum}")
            self.toplevel.title("Cập nhật thông tin bàn")
            btn_save.configure(text="Cập nhật")
            self.table_num_value.set(self.__table_selected.tableNum)
            self.seat_num_value.set(self.__table_selected.seatNum)
            if self.__table_selected.status == 0:
                self.status_combox.set(StatusTable.AVAILABLE.value)
            else:
                self.status_combox.set(StatusTable.DISABLED.value)

        table_popup_frame.pack(fill=tk.BOTH, expand=1)


    def create_menu_option_right(self, window):
        self.context_menu = tk.Menu(window, tearoff=0)
        self.context_menu.add_command(label="Chỉnh sửa", command=lambda: self.edit_table(window=window))
        self.context_menu.add_command(label="Xóa", command=lambda: self.delete_table(window=window))
        self.context_menu.add_separator()


    def __show_context_popup(self, event, tableSelected: Table):
        self.__table_selected = tableSelected
        if self.__user_type == UserType.ADMIN and tableSelected.table_type == TableType.Normal:
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
                print(f"ss {self.__table_selected.tableNum}")
            finally:
                self.context_menu.grab_release()

    def edit_table(self, window):
        self.create_ui_toplevel(window, Action.UPDATE)

    def delete_table(self, window):
        print(f"dd {self.__table_selected.tableNum}")
        self.__controller.delete_and_reload(table_id=self.__table_selected.id)
        for item in self.grid_content.winfo_children():
            item.destroy()
        self._add_content(window, self.__controller.tables)
        self.__table_selected = None
    def validate_input(self, new_value):
        # Kiểm tra xem giá trị mới có phải là số không
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def click_button_add_or_edit_popup(self, window, action_type):
        table_status = 0
        if self.status_combox.get() == StatusTable.DISABLED.value:
            table_status = 1
        print(table_status)
        if (self.table_num_value.get() == '' or self.table_num_value.get() == '0'
                and self.seat_num_value.get() == '' or self.seat_num_value.get() == '0'):
            self.lb_validate_table_info.configure(text="Vui lòng điền đầy đủ thông tin")
            return
        else:
            if action_type == Action.ADD:
                print(f"add table_num_value {self.table_num_value}")
                # Thực hiện thêm vào database
                self.__controller.add_new_and_reload(table_num_value=self.table_num_value.get(),
                                                     seat_num_value=int(self.seat_num_value.get()),
                                                     status_value=table_status)
            else:
                # Thực hiện cập nhật lại database
                self.__controller.update_and_reload(id=self.__table_selected.id,
                                                    table_num_value=self.table_num_value.get(),
                                                    seat_num_value=int(self.seat_num_value.get()),
                                                    status_value=table_status)

            self.toplevel.destroy()
        # Thực hiện reload lại UI danh sách bàn
        self._add_content(window=window, tables=self.__controller.tables)


