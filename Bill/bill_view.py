from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter
import ttkbootstrap as bt
from customtkinter import *


class BillView:
    def __init__(self, window, controller):
        self.__controller = controller
        self.__date_variable = tk.StringVar()
        self.__date_variable.set(f"{datetime.now():%d/%m/%Y}")
        self.__creator_name_var = tk.StringVar()
        self.__customer_name_var = tk.StringVar()
        self.__phone_var = tk.StringVar()
        self.__bill_created_date_var = tk.StringVar()
        self.__table_num_var = tk.StringVar()
        self.__discount_var = tk.StringVar()
        self.__bill_type_var = tk.StringVar()
        self.__money_var = tk.StringVar()
        # Setup UI
        self.phone_validation = window.register(self.validate_phone_number_input)
        self.__generate_ui_content(window)

    def __generate_ui_content(self, window):
        customtkinter.set_appearance_mode("light")
        style = ttk.Style()
        style.theme_use('default')
        main_fr = CTkFrame(window)
        main_fr.pack(fill=tk.BOTH, expand=1)
        self.ui_header(main_fr)
        # UI TreeView
        self.tv = ttk.Treeview(main_fr)
        self.tv.pack(fill=tk.X, expand=0, padx=10, pady=10)
        style.configure("Treeview.Heading", background="DodgerBlue1", forceground="white", font=("TkDefaultFont", 18))
        self.tv["columns"] = (
            "id", "user_create", "customer_name", "customer_phone", "table_num", "create_date", "bill_type",
            "total_money", "update_date")
        self.tv["show"] = "headings"
        self.tv.column("id", anchor="center", width=50)
        self.tv.column("user_create", anchor="center", width=140)
        self.tv.column("customer_name", anchor="center", width=160)
        self.tv.column("customer_phone", anchor="center", width=140)
        self.tv.column("table_num", anchor="center", width=100)
        self.tv.column("create_date", anchor="center", width=100)
        self.tv.column("bill_type", anchor="center", width=60)
        self.tv.column("total_money", anchor="center", width=160)
        self.tv.column("update_date", anchor="center", width=100)

        self.tv.heading("id", text="ID")
        self.tv.heading("user_create", text="Tên người Tạo")
        self.tv.heading("customer_name", text="Tên Khách Hàng")
        self.tv.heading("customer_phone", text="SDT Khách Hàng")
        self.tv.heading("table_num", text="Số Bàn")
        self.tv.heading("create_date", text="Ngày Tạo")
        self.tv.heading("bill_type", text="Loại")
        self.tv.heading("total_money", text="Tổng Tền")
        self.tv.heading("update_date", text="Ngày cập nhật")
        self.tv.tag_configure("normal", background="white")
        self.tv.tag_configure("blue", background="lightblue")

        # Fill data vào treeview
        self.__insert_column_values()
        self.tv.bind("<<TreeviewSelect>>", lambda e: self.item_treeview_selected())

        self.__ui_detail_form(main_fr, window)

    def ui_header(self, main_fr):
        option_fr = CTkFrame(main_fr, fg_color="transparent")
        option_fr.pack(fill=tk.X, expand=0, pady=10, padx=20)
        lb_date = CTkLabel(option_fr, text="Ngày tạo")
        lb_date.pack(fill=tk.X, expand=0, side="left", padx=5)

        date_entry = bt.DateEntry(option_fr, dateformat="%d/%m/%Y", bootstyle="primary")
        date_entry.entry.configure(textvariable=self.__date_variable)
        self.__date_variable.trace('w',
                                   lambda name, index, mode,
                                          date_value=self.__date_variable: self.change_date_reload_view())
        date_entry.pack(side="left")

        group_option = CTkFrame(option_fr)
        group_option.pack(side="right", ipadx=5)
        add_btn = CTkButton(group_option,
                            text="Thêm mới",
                            corner_radius=18,
                            border_width=0,
                            height=36,
                            fg_color="DodgerBlue1",
                            hover_color="#63B8FF",
                            text_color="black",
                            font=CTkFont("TkDefaultFont", 16),
                            command=lambda: self.add_click())
        add_btn.pack(fill=tk.X, expand=0, side="left")

        update_btn = CTkButton(group_option,
                               text="Chỉnh sửa",
                               corner_radius=18,
                               border_width=0,
                               height=36,
                               fg_color="LimeGreen",
                               hover_color="#54FF9F",
                               text_color="black",
                               font=CTkFont("TkDefaultFont", 16),
                               command=lambda: self.update_click())
        update_btn.pack(fill=tk.X, expand=0, side="left", padx=5)

        delete_btn = CTkButton(group_option,
                               text="Xóa",
                               corner_radius=18,
                               border_width=0,
                               height=36,
                               fg_color="Firebrick1",
                               hover_color="#FFC0CB",
                               text_color="black",
                               font=CTkFont("TkDefaultFont", 16),
                               command=lambda: self.delete_click())
        delete_btn.pack(fill=tk.X, expand=0, side="left")

    def __ui_detail_form(self, main_fr, window):
        padding_x = 25
        padding_y = 5
        entry_width = 300
        entry_padding_y = 5

        detail_fr = CTkFrame(main_fr, border_width=2,
                             fg_color="white",
                             corner_radius=10, border_color="gray")
        detail_fr.pack(fill=tk.Y, expand=1, padx=20, pady=5)

        detail_lb = CTkLabel(detail_fr, text="Thông tin chi tiết", text_color="#000088",
                             font=CTkFont("TkDefaultFont", 16, 'bold'))
        detail_lb.pack(fill=tk.X, expand=0, padx=20, side="top", pady=5)

        self.sub_fr = CTkFrame(detail_fr, fg_color="white")
        self.sub_fr.pack(fill=tk.X, expand=0, padx=padding_x, pady=padding_y, ipadx=10)
        self.sub_fr.columnconfigure(0, weight=1)
        self.creator_name_lb = CTkLabel(self.sub_fr, text="Tên người tạo",
                                        font=CTkFont("TkDefaultFont", 14, 'bold'),
                                        anchor=tk.W)
        self.creator_name_lb.grid(row=0, column=0, sticky=tk.NW)
        creator_name_entry = CTkEntry(self.sub_fr,
                                      textvariable=self.__creator_name_var,
                                      placeholder_text="Nhập họ tên người tạo",
                                      width=entry_width)
        creator_name_entry.grid(row=0, column=1, sticky=(tk.N, tk.W), pady=entry_padding_y)

        self.customer_name_lb = CTkLabel(self.sub_fr, text="Họ tên khách hàng", anchor=tk.W,
                                         font=CTkFont("TkDefaultFont", 14, 'bold'))
        self.customer_name_lb.grid(row=1, column=0, sticky=tk.NW)
        customer_name_entry = CTkEntry(self.sub_fr,
                                       textvariable=self.__customer_name_var,
                                       placeholder_text="Nhập họ tên khách hàng",
                                       width=entry_width)
        customer_name_entry.grid(row=1, column=1, sticky=tk.NW, pady=entry_padding_y)

        customer_phone_lb = CTkLabel(self.sub_fr, text="Số điện thoại khách hàng", anchor=tk.W,
                                     font=CTkFont("TkDefaultFont", 14, 'bold'))
        customer_phone_lb.grid(row=2, column=0, sticky=tk.NW)

        customer_phone_entry = CTkEntry(self.sub_fr,
                                        textvariable=self.__phone_var,
                                        placeholder_text="Nhập số điện thoại",
                                        width=entry_width,
                                        validate="key",
                                        validatecommand=(self.phone_validation, '%P'))
        customer_phone_entry.grid(row=2, column=1, sticky=tk.NW, pady=entry_padding_y)

        created_date_lb = CTkLabel(self.sub_fr, text="Ngày tạo", anchor=tk.W,
                                   font=CTkFont("TkDefaultFont", 14, 'bold'))
        created_date_lb.grid(row=3, column=0, sticky=tk.NW)
        created_date_entry = bt.DateEntry(self.sub_fr, dateformat="%d/%m/%Y", bootstyle="primary")
        created_date_entry.grid(row=3, column=1, sticky=tk.NW, pady=entry_padding_y)
        created_date_entry.entry.configure(textvariable=self.__bill_created_date_var)

        table_lb = CTkLabel(self.sub_fr, text="Số bàn", anchor=tk.W, font=CTkFont("TkDefaultFont", 14, 'bold'))
        table_lb.grid(row=4, column=0, sticky=tk.NW)
        self.table_cbb = CTkComboBox(self.sub_fr,
                                     width=entry_width,
                                     button_color="DodgerBlue2",
                                     values=["Unknow"],
                                     state="readonly",
                                     variable=self.__table_num_var)
        self.table_cbb.grid(row=4, column=1, sticky=tk.NW, pady=entry_padding_y)
        self.set_values_table_cbb(self.table_cbb)
        bill_type_lb = CTkLabel(self.sub_fr, text="Loại hóa đơn", anchor=tk.W,
                                font=CTkFont("TkDefaultFont", 14, 'bold'))
        bill_type_lb.grid(row=5, column=0, sticky=tk.NW)

        bill_type_cbb = CTkComboBox(self.sub_fr,
                                    width=150,
                                    button_color="DodgerBlue2",
                                    variable=self.__bill_type_var,
                                    values=["Thu", "Chi"])
        bill_type_cbb.grid(row=5, column=1, sticky=tk.NW, pady=entry_padding_y)

        discount_lb = CTkLabel(self.sub_fr, text="Khuyến mãi", anchor=tk.W,
                               font=CTkFont("TkDefaultFont", 14, 'bold'))
        discount_lb.grid(row=6, column=0, sticky=tk.NW)

        self.discount_cbb = CTkComboBox(self.sub_fr,
                                        width=entry_width,
                                        button_color="DodgerBlue2",
                                        variable=self.__discount_var,
                                        state="readonly",
                                        values=["Unknow"])
        self.discount_cbb.grid(row=6, column=1, sticky=tk.NW, pady=entry_padding_y)
        self.set_values_discount_cbb(self.discount_cbb)
        self.money_lb = CTkLabel(self.sub_fr, text="Tổng tiền", anchor=tk.W,
                                 font=CTkFont("TkDefaultFont", 14, 'bold'))
        self.money_lb.grid(row=7, column=0, sticky=tk.NW)
        money_entry = CTkEntry(self.sub_fr,
                               textvariable=self.__money_var,
                               width=entry_width,
                               placeholder_text="Nhập tổng tiền",
                               placeholder_text_color="gray",
                               validate="key",
                               validatecommand=(self.phone_validation, '%P'))
        money_entry.grid(row=7, column=1, sticky=tk.NW, pady=entry_padding_y)
        self.valid_lb = CTkLabel(master=detail_fr,
                                 text="Vui lòng nhập tổng tiền",
                                 font=CTkFont("TkDefaultFont", 14),
                                 text_color="red",
                                 anchor=tk.CENTER)
        self.valid_lb.pack(fill=tk.BOTH, expand=0, padx=padding_x, pady=padding_y)
        self.hidden_validate()

    def hidden_validate(self):
        self.valid_lb.pack_forget()
        self.valid_lb.update_idletasks()

    def show_validate(self, valid_text):
        padding_x = 25
        padding_y = 5
        self.valid_lb.configure(text=valid_text)
        self.valid_lb.pack(fill=tk.BOTH, expand=0, padx=padding_x, pady=padding_y)
        self.valid_lb.update_idletasks()

    def change_date_reload_view(self):
        if self.__date_variable.get() != '':
            for item in self.tv.get_children():
                self.tv.delete(item)
            self.__insert_column_values(datetime.strptime(self.__date_variable.get(), "%d/%m/%Y"))

    def __insert_column_values(self, by_date=datetime.now()):
        my_tag = "blue"
        bills = self.__controller.get_data(by_date)
        for b in bills:
            if my_tag == "normal":
                my_tag = "blue"
            else:
                my_tag = "normal"
            # ("id", "user_create", "customer_name", "customer_phone", "table_num", "create_date", "bill_type",
            #     "total_money", "update_date")
            user_name = self.__controller.get_user_name_by_id(b.userId)
            if user_name or user_name == "":
                user_name = b.creatorName
            table_num = ""
            self.tv.insert("", "end", iid=b.id, text=b.id,
                           values=(b.id, user_name, b.customerName, b.customerPhoneNumber,
                                   table_num, b.createdDate, "Thu", b.totalMoney, b.updatedDate),
                           tags=my_tag)

    def add_click(self):
        valid_text = ""
        is_validate = lambda text: 0 if len(text) == 0 or text.isspace() == 1 else 1
        if not is_validate(self.__creator_name_var.get()):
            valid_text = f"Vui lòng nhập" + f" {self.creator_name_lb.cget("text")}"
        if not is_validate(self.__customer_name_var.get()):
            if len(valid_text) == 0:
                valid_text = f"Vui lòng nhập" + f" {self.customer_name_lb.cget("text")}"
            else:
                valid_text = valid_text + f", {self.customer_name_lb.cget("text")}"

        if not is_validate(self.__money_var.get()):
            if len(valid_text) == 0:
                valid_text = f"Vui lòng nhập" + f" {self.money_lb.cget("text")}"
            else:
                valid_text = valid_text + f", {self.money_lb.cget("text")}"

        if valid_text:
            self.show_validate(valid_text)
        else:
            self.__controller.add_new_bill_and_reload()
            self.reload_treeview()

    def update_click(self):
        selected_items = self.tv.selection()
        if not selected_items:
            messagebox.showwarning("Thông báo", "Vui lòng chọn dòng muốn chỉnh sửa.")
            return
        for item in selected_items:
            item_id = self.tv.item(item, "values")[0]
            self.__controller.update_and_reload(_id=item_id)
        self.reload_treeview()

    def delete_click(self):
        selected_items = self.tv.selection()
        if not selected_items:
            messagebox.showwarning("Thông báo", "Vui lòng chọn dòng muốn xóa.")
            return
        if messagebox.askokcancel(title="Thông báo", message="Bạn có chắc chắn muốn xóa sản phẩm này không?"):
            for item in selected_items:
                item_id = self.tv.item(item, "values")[0]
                self.tv.delete(item)
                self.__controller.delete_and_reload(_id=item_id)
            self.reload_treeview()

    def reload_treeview(self):
        for item in self.tv.get_children():
            self.tv.delete(item)
        self.__insert_column_values()

    def get_detail_form_values(self):
        return {"customerName": self.__customer_name_var.get(),
                "customerPhoneNumber": self.__phone_var.get(),
                "creator_name": self.__creator_name_var.get(),
                "discount_id": 0,
                "table_num": self.__table_num_var.get(),
                "bill_type": self.__bill_type_var.get(),
                "totalMoney": self.__money_var.get(),
                "created_date": self.__bill_created_date_var.get()}

    def validate_phone_number_input(self, new_value):
        print(new_value)
        try:
            if str.isdigit(new_value) and len(new_value) <= 10:
                return True
            else:
                return False

        except ValueError:
            return False

    def set_values_table_cbb(self, table_cbb: CTkComboBox):
        dict_tables = self.__controller.get_tables()
        if len(dict_tables.values()) > 0:
            table_cbb.configure(values=dict_tables.values())

    def set_values_discount_cbb(self, discount_cbb: CTkComboBox):
        dict_discount = self.__controller.get_discounts()
        if len(dict_discount.values()) > 0:
            discount_cbb.configure(values=dict_discount.values())

    def item_treeview_selected(self):
        self.discount_cbb.configure(state="disable")
        self.table_cbb.configure(state="disable")
        selected_items = self.tv.selection()
        for item in selected_items:
            rows = self.tv.item(item, "values")
            self.__creator_name_var.set(rows[1])
            self.__customer_name_var.set(rows[2])
            self.__phone_var.set(rows[3])
            self.__table_num_var.set(rows[4])
            self.__bill_created_date_var.set(rows[5])
            self.__bill_type_var.set(rows[6])
            self.__money_var.set(rows[7])
            print(item)
