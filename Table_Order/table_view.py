import math
import tkinter as tk
from enum import Enum
import customtkinter as ctk
from PIL import Image
from Table_Order.table_model import TableType, Table
from share.common_config import Action, UserType
from share.utils import Utils
from tkinter import ttk


class StatusTable(Enum):
    DISABLED = "Đã đặt"
    AVAILABLE = "Trống"


class TableView:
    hover_color = "LightSkyBlue"

    def __init__(self, window, controller, user_type):
        # property
        self.__controller = controller
        self.__user_type = user_type
        self.table_num_value = tk.StringVar()
        self.seat_num_value = tk.StringVar()
        self.status_value = tk.StringVar()
        self.__table_selected = Table()
        self.__screen_width = window.winfo_width()
        self.__screen_height = window.winfo_height()
        self.status_cbb_var = tk.StringVar()

        self.grid_frame = ctk.CTkFrame(window)
        self.grid_frame.pack(fill="both", expand=True)

        # Utils.set_appearance_mode(ctk)
        ctk.set_appearance_mode("light")

        # Tạo thanh cuộn ngang
        self.horizontal_scrollbar = ctk.CTkScrollbar(self.grid_frame, orientation="horizontal")
        self.horizontal_scrollbar.pack(side="bottom", fill="x")

        # Tạo thanh cuộn dọc
        self.vertical_scrollbar = ctk.CTkScrollbar(self.grid_frame, orientation="vertical")
        self.vertical_scrollbar.pack(side="right", fill="y")

        # Tạo một canvas để chứa lưới
        self.canvas = ctk.CTkCanvas(self.grid_frame, xscrollcommand=self.horizontal_scrollbar.set,
                                    yscrollcommand=self.vertical_scrollbar.set)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # Kết nối thanh cuộn với canvas
        self.horizontal_scrollbar.configure(command=self.canvas.xview)
        self.vertical_scrollbar.configure(command=self.canvas.yview)

        # Tạo một frame con để chứa bàn
        self.grid_content = ctk.CTkFrame(self.canvas, fg_color="white")
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
                    table_fr = ctk.CTkFrame(self.grid_content)
                    table_fr.grid(row=i, column=j, sticky="nsew", padx=5, pady=5,
                                  ipadx=column_width // 4,
                                  ipady=row_height // 4)
                    img_table = ctk.CTkImage(Image.open("../../assets/ic_table_visible.png"),
                                             size=(image_size, image_size))
                    btn = ctk.CTkLabel(table_fr, text=num_table, image=img_table, font=ctk.CTkFont("TkDefaultFont", 18))
                    btn.bind("<Button-1>", lambda e, t=tables[index]: self.selected_table(window, t))
                    btn.bind("<Button-2>",
                             lambda e, t=tables[index]: self.__show_context_popup(event=e, tableSelected=t))
                    btn.pack(fill=tk.BOTH, expand=1)

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
        global toplevel, entry_table_num, entry_seat_num, status_combox, lb_validate_table_info

        toplevel = ctk.CTkToplevel(window)
        toplevel.resizable(True, False)
        toplevel.geometry("290x250")
        validation = window.register(self.validate_input)
        table_popup_frame = ctk.CTkFrame(toplevel)
        lb_table_num = ctk.CTkLabel(table_popup_frame, text="Số bàn")
        lb_table_num.place(x=10, y=20)
        entry_table_num = ctk.CTkEntry(table_popup_frame,
                                       textvariable=self.table_num_value,
                                       border_width=1,
                                       border_color="gray",
                                       validate="key", fg_color=("white", "white"))
        entry_table_num.place(x=80, y=20)

        lb_seat_num = ctk.CTkLabel(table_popup_frame, text="Số ghế")
        lb_seat_num.place(x=10, y=60)
        entry_seat_num = ctk.CTkEntry(table_popup_frame, textvariable=self.seat_num_value, validate="key",
                                      validatecommand=(validation, '%P'),
                                      fg_color="white",
                                      border_width=1, border_color="gray", state="normal")

        entry_seat_num.place(x=80, y=60)

        lb_table_status = ctk.CTkLabel(table_popup_frame, text="Trạng thái")
        lb_table_status.place(x=10, y=100)
        status_combox = ctk.CTkComboBox(table_popup_frame,
                                        border_width=1,
                                        values=[StatusTable.AVAILABLE.value, StatusTable.DISABLED.value],
                                        state="readonly", variable=self.status_cbb_var)
        status_combox.place(x=80, y=100)
        lb_validate_table_info = ctk.CTkLabel(table_popup_frame, text="", text_color="red")
        lb_validate_table_info.place(x=60, y=140)

        btn_save = ctk.CTkButton(table_popup_frame, text="Lưu",
                                 command=lambda: self.click_button_add_or_edit_popup(window, action_type))
        btn_save.pack(fill=tk.Y, expand=0, side="bottom", pady=40)
        if action_type == Action.ADD:
            self.table_num_value.set("")
            self.seat_num_value.set("")
            toplevel.title("Thêm bàn mới")
            self.status_cbb_var.set(StatusTable.AVAILABLE.value)
            btn_save.configure(text="Lưu")
        else:
            toplevel.title("Cập nhật thông tin bàn")
            btn_save.configure(text="Cập nhật")
            self.table_num_value.set(self.__table_selected.tableNum)
            self.seat_num_value.set(self.__table_selected.seatNum)
            if self.__table_selected.status == 0:
                self.status_cbb_var.set(StatusTable.AVAILABLE.value)
            else:
                self.status_cbb_var.set(StatusTable.DISABLED.value)

        table_popup_frame.pack(fill=tk.BOTH, expand=1)

    def create_menu_option_right(self, window):
        global context_menu
        context_menu = tk.Menu(window, tearoff=0)
        context_menu.add_command(label="Chỉnh sửa", command=lambda: self.edit_table(window=window))
        context_menu.add_command(label="Xóa", command=lambda: self.delete_table(window=window))
        context_menu.add_separator()

    def __show_context_popup(self, event, tableSelected: Table):
        self.__table_selected = tableSelected
        if self.__user_type == UserType.ADMIN and tableSelected.table_type == TableType.Normal:
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
                print(f"ss {self.__table_selected.tableNum}")
            finally:
                context_menu.grab_release()

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
        if self.status_cbb_var.get() == StatusTable.DISABLED.value:
            table_status = 1
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

            toplevel.destroy()
        # Thực hiện reload lại UI danh sách bàn
        self._add_content(window=window, tables=self.__controller.tables)
