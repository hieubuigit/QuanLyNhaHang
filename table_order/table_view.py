import math
import tkinter as tk
from enum import Enum
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from entities.models import Table
from share.common_config import Action, UserType, StatusTable, TableType
from share.utils import Utils


class TableView:
    hover_color = "LightSkyBlue"

    def __init__(self, window, controller, user_type):
        # property
        self._window = window
        self._controller = controller
        self.__user_type = user_type
        self._table_num_value = tk.StringVar()
        self._seat_num_value = tk.StringVar()
        self._status_value = tk.StringVar()
        self.__table_selected = None
        self.__screen_width = window.winfo_width()
        self.__screen_height = window.winfo_height()
        self.status_cbb_var = tk.StringVar(value=StatusTable.AVAILABLE.value[1])

        # Utils.set_appearance_mode(ctk)
        # Setup UI
        self.create_ui(window)
        # Thêm ds bàn vào grid content
        self._add_content(self._controller.tables)

    def create_ui(self, master):
        global grid_content
        grid_frame = ctk.CTkFrame(master, fg_color="white")
        grid_frame.pack(fill="both", expand=True)

        # Tạo thanh cuộn ngang
        horizontal_scrollbar = ctk.CTkScrollbar(grid_frame, orientation="horizontal")
        horizontal_scrollbar.pack(side="bottom", fill="x")

        # Tạo thanh cuộn dọc
        vertical_scrollbar = ctk.CTkScrollbar(grid_frame, orientation="vertical")
        vertical_scrollbar.pack(side="right", fill="y")

        # Tạo một canvas để chứa lưới
        canvas = ctk.CTkCanvas(grid_frame, xscrollcommand=horizontal_scrollbar.set,
                               yscrollcommand=vertical_scrollbar.set, background="white")
        canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # Kết nối thanh cuộn với canvas
        horizontal_scrollbar.configure(command=canvas.xview)
        vertical_scrollbar.configure(command=canvas.yview)

        # Tạo một frame con để chứa bàn
        grid_content = ctk.CTkFrame(canvas, fg_color="white")
        canvas.create_window((0, 0), window=grid_content, anchor="nw")

        # Đặt sự kiện để cập nhật kích thước của canvas
        grid_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.create_menu_option_right(master)

    def _add_content(self, tables):
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
                    num_table = tables[index].tableNum
                    grid_content.grid_columnconfigure(j, weight=1)
                    table_fr = ctk.CTkFrame(grid_content)
                    table_fr.grid(row=i, column=j, sticky="nsew", padx=5, pady=5,
                                  ipadx=column_width // 4,
                                  ipady=row_height // 4)

                    img_table = ctk.CTkImage(Image.open("../assets/ic_table_visible.png"),
                                             size=(image_size, image_size))
                    btn = ctk.CTkLabel(table_fr, text=num_table, image=img_table,
                                       font=ctk.CTkFont("TkDefaultFont", 18), fg_color="#EEEEEE")
                    if tables[index].status == StatusTable.DISABLED.value[0]:
                        img_table_disable = ctk.CTkImage(Image.open("../assets/ic_table_disable.png"),
                                                         size=(image_size, image_size))
                        btn.configure(image=img_table_disable)
                    btn.bind("<Button-1>", lambda e, t=tables[index]: self.selected_table(t))
                    btn.bind("<Button-2>",
                             lambda e, t=tables[index]: self.__show_context_popup(event=e, tableSelected=t))
                    btn.pack(fill=tk.BOTH, expand=1)

    def selected_table(self, table):
        self.__table_selected = table
        if self.__user_type == UserType.ADMIN.value:
            if table.table_type == TableType.Add:
                self.create_ui_add_toplevel(self._window, Action.ADD)
        else:
            # order
            if table.status == StatusTable.AVAILABLE.value[0]:
                if messagebox.askokcancel("Thông báo", "Xác nhận đặt bàn và bắt đầu chọn món"):
                    if self._controller.create_bill(id_table=table.id, id_user=Utils.user_profile["id"]):
                        self.reload_ui_table(table_id=table.id, status=StatusTable.DISABLED.value[0])
                        self._controller.show_menu_food(view_master=self._window,
                                                        reload_table_page=self.reload_table_page,
                                                        table=table)
            else:
                if self._controller.check_my_bill(table_id=table.id):
                    self._controller.show_menu_food(view_master=self._window,
                                                    reload_table_page=self.reload_table_page,
                                                    table=table)

    def reload_table_page(self):
        self.reload_ui_table(self.__table_selected.id, status=StatusTable.AVAILABLE.value[0])

    def reload_ui_table(self, table_id, status):
        if self._controller.update_table_status(id_table=table_id,
                                                status=status):
            for item in grid_content.winfo_children():
                item.destroy()
            self._add_content(self._controller.tables)

    def create_ui_add_toplevel(self, window, action_type):
        global toplevel

        toplevel = ctk.CTkToplevel(window)
        toplevel.resizable(True, False)
        toplevel.geometry("300x250")

        validation = window.register(self.validate_input)
        table_popup_frame = ctk.CTkFrame(toplevel, fg_color="white")

        sub_fr = ctk.CTkFrame(table_popup_frame, fg_color="white")
        sub_fr.pack(fill=tk.BOTH, expand=1)
        lb_table_num = ctk.CTkLabel(sub_fr, text="Số bàn")
        lb_table_num.grid(row=0, column=0, padx=(30, 15), pady=(30, 15), sticky="w")
        entry_table_num = ctk.CTkEntry(sub_fr,
                                       textvariable=self._table_num_value,
                                       border_width=1,
                                       border_color="gray",
                                       validate="key", fg_color=("white", "white"))
        entry_table_num.grid(row=0, column=1, pady=(30, 15))

        lb_seat_num = ctk.CTkLabel(sub_fr, text="Số ghế")
        lb_seat_num.grid(row=1, column=0, sticky="w", padx=(30, 15))
        entry_seat_num = ctk.CTkEntry(sub_fr, textvariable=self._seat_num_value, validate="key",
                                      validatecommand=(validation, '%S'),
                                      fg_color="white",
                                      border_width=1, border_color="gray", state="normal")
        entry_seat_num.grid(row=1, column=1)

        lb_table_status = ctk.CTkLabel(sub_fr, text="Trạng thái")
        lb_table_status.grid(row=2, column=0, padx=(30, 15), pady=(15, 0), sticky="w")
        status_combox = ctk.CTkComboBox(sub_fr,
                                        border_width=1,
                                        values=[StatusTable.AVAILABLE.value[1], StatusTable.DISABLED.value[1]],
                                        state=tk.DISABLED, variable=self.status_cbb_var)
        status_combox.grid(row=2, column=1, pady=(15, 0))
        btn_save = ctk.CTkButton(table_popup_frame, text="Lưu", height=35, width=100,
                                 command=lambda: self.click_button_add_or_edit_popup(action_type))
        btn_save.pack(expand=0, pady=(0, 30))

        if action_type == Action.ADD:
            toplevel.title("Thêm bàn mới")
            btn_save.configure(text="Lưu")
        else:
            toplevel.title("Cập nhật thông tin bàn")
            btn_save.configure(text="Cập nhật")
            self._table_num_value.set(self.__table_selected.tableNum)
            self._seat_num_value.set(self.__table_selected.seatNum)
            if self.__table_selected.status == 0:
                self.status_cbb_var.set(StatusTable.AVAILABLE.value[1])
            else:
                self.status_cbb_var.set(StatusTable.DISABLED.value[1])

        table_popup_frame.pack(fill=tk.BOTH, expand=1)

    def create_menu_option_right(self, window):
        global context_menu
        context_menu = tk.Menu(window, tearoff=0)
        context_menu.add_command(label="Chỉnh sửa", command=lambda: self.edit_table(window=window))
        context_menu.add_command(label="Xóa", command=lambda: self.delete_table(window=window))
        context_menu.add_separator()

    def __show_context_popup(self, event, tableSelected: Table):
        if tableSelected.status == StatusTable.AVAILABLE.value[0]:
            self.__table_selected = tableSelected
            if self.__user_type == UserType.ADMIN.value and tableSelected.table_type == TableType.Normal:
                try:
                    context_menu.tk_popup(event.x_root, event.y_root)
                finally:
                    context_menu.grab_release()

    def edit_table(self, window):
        self.create_ui_add_toplevel(window, Action.UPDATE)

    def delete_table(self, window):
        self._controller.delete_and_reload(table_id=self.__table_selected.id)
        for item in grid_content.winfo_children():
            item.destroy()
        self._add_content(self._controller.tables)
        self.__table_selected = None

    def click_button_add_or_edit_popup(self, action_type):
        table_status = 0
        if self.status_cbb_var.get() == StatusTable.DISABLED.value[1]:
            table_status = 1
        else:
            table_status = 0

        if (self._table_num_value.get().isspace() or self._table_num_value.get() == ''
                or self._table_num_value.get() == '0'
                or self._seat_num_value.get() == '0' or self._seat_num_value.get() == ''):
            messagebox.showinfo("", "Vui lòng điền đầy đủ thông tin")
            return
        else:
            if action_type == Action.ADD:
                # Thực hiện thêm vào database
                if self._controller.add_new_and_reload(table_num_value=self._table_num_value.get(),
                                                       seat_num_value=self._seat_num_value.get(),
                                                       status_value=table_status):
                        self.clear_entry_value_toplevel()
                        toplevel.destroy()
            else:
                # Thực hiện cập nhật lại database
                if self._controller.update_and_reload(id=self.__table_selected.id,
                                                      table_num_value=self._table_num_value.get(),
                                                      seat_num_value=self._seat_num_value.get(),
                                                      status_value=table_status):
                        self.clear_entry_value_toplevel()
                        toplevel.destroy()
        # Thực hiện reload lại UI danh sách bàn
        self._add_content(tables=self._controller.tables)

    def clear_entry_value_toplevel(self):

        if self._table_num_value is not None:
            self._table_num_value.set("")
        if self._seat_num_value is not None:
            self._seat_num_value.set("")

    def validate_input(self, text):
        # Chỉ cho phép chữ số
        if text.isdigit():
            return True
        else:
            return False
