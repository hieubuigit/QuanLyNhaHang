from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from entities.models import Billing
from share.CEntryDate import CEntryDate
from share.common_config import BillType, BillStatus, UserType
from share.utils import Utils
from tkinter import ttk
from PIL import Image


class BillView:
    def __init__(self, window, controller):
        self.__root = window
        self.__controller = controller
        self.__customer_name_var = tk.StringVar()
        self.__phone_var = tk.StringVar()
        self.__bill_status_var = tk.StringVar()
        self.__bill_type_var = tk.StringVar()
        self.__money_var = tk.StringVar()
        self.__bill_type_dict = {BillType.REVENUE.value[0]: BillType.REVENUE.value[1],
                                 BillType.EXPANDING.value[0]: BillType.EXPANDING.value[1]}
        self.__status_values = {BillStatus.PAID.value: "Đã thanh toán", BillStatus.UNPAID.value: "Chưa thanh toán"}
        self.__bill_id_selected = None
        self._user_type = Utils.user_profile["type"]
        # Setup UI
        self._phone_validation = window.register(self.validate_phone_number_input)
        self._money_validation = window.register(self.validation_money_input)
        self.__generate_ui_content(window)

    def __generate_ui_content(self, window):
        style = ttk.Style()
        main_fr = ctk.CTkFrame(window)
        main_fr.pack(fill=tk.BOTH, expand=1)

        self.ui_header(main_fr)

        # UI TreeView
        self.tv = ttk.Treeview(main_fr)
        self.tv.pack(fill=tk.X, expand=0, padx=10, pady=10)

        style.configure("Custom.Treeview.Heading", background="DodgerBlue1", forceground="white", font=("TkDefaultFont", 18))
        self.tv["columns"] = (
            "id", "user_create", "customer_name", "customer_phone", "table_num", "create_date", "bill_type",
            "total_money", "status")
        self.tv["show"] = "headings"
        self.tv.column("id", anchor="center", width=50)
        self.tv.column("user_create", anchor="center", width=140)
        self.tv.column("customer_name", anchor="center", width=160)
        self.tv.column("customer_phone", anchor="center", width=140)
        self.tv.column("table_num", anchor="center", width=100)
        self.tv.column("create_date", anchor="center", width=100)
        self.tv.column("bill_type", anchor="center", width=60)
        self.tv.column("total_money", anchor="center", width=160)
        self.tv.column("status", anchor="center", width=100)

        self.tv.heading("id", text="ID")
        self.tv.heading("user_create", text="Tên người Tạo")
        self.tv.heading("customer_name", text="Tên Khách Hàng")
        self.tv.heading("customer_phone", text="SDT Khách Hàng")
        self.tv.heading("table_num", text="Số Bàn")
        self.tv.heading("create_date", text="Ngày Tạo")
        self.tv.heading("bill_type", text="Loại")
        self.tv.heading("total_money", text="Tổng Tền")
        self.tv.heading("status", text="Trạng thái")
        self.tv.tag_configure("normal", background="white")
        self.tv.tag_configure("blue", background="lightblue")

        # Fill data vào treeview
        self.__insert_column_values()
        if self._user_type == UserType.ADMIN.value:
            self.tv.bind("<<TreeviewSelect>>", lambda e: self.item_treeview_selected())
            self.__ui_detail_form(main_fr)

    def ui_header(self, main_fr):
        global date_entry_filter
        option_fr = ctk.CTkFrame(main_fr, fg_color="transparent")
        option_fr.pack(fill=tk.X, expand=0, pady=10, padx=20)
        date_group_fr = ctk.CTkFrame(option_fr)
        date_group_fr.pack(fill=tk.X, expand=0, side=tk.LEFT, anchor=tk.NW)
        lb_date = ctk.CTkLabel(date_group_fr, text="Ngày tạo")
        lb_date.pack(fill=tk.X, expand=0, side="left", anchor="nw", padx=5)

        date_entry_filter = CEntryDate(date_group_fr)
        date_entry_filter.pack(side="left", anchor="nw")
        ic_filter = ctk.CTkImage(Image.open("../assets/funnel.png"), size=(20, 20))
        filter_btn = ctk.CTkButton(date_group_fr, text="", image=ic_filter, width=50, height=28, fg_color="white",
                                   border_width=1, border_color="gray",
                                   hover_color="#63B8FF",
                                   command=lambda: self.change_date_reload_view())
        filter_btn.pack(expand=0, padx=5)
        if self._user_type == UserType.ADMIN.value:
            group_option = ctk.CTkFrame(option_fr)
            group_option.pack(side="right", ipadx=5)
            add_btn = ctk.CTkButton(group_option,
                                    text="Thêm",
                                    corner_radius=18,
                                    border_width=0,
                                    height=36,
                                    fg_color="DodgerBlue1",
                                    hover_color="#63B8FF",
                                    text_color="black",
                                    font=ctk.CTkFont("TkDefaultFont", 16),
                                    command=lambda: self.add_click())
            add_btn.pack(fill=tk.X, expand=0, side="left")

            update_btn = ctk.CTkButton(group_option,
                                       text="Cập nhật",
                                       corner_radius=18,
                                       border_width=0,
                                       height=36,
                                       fg_color="LimeGreen",
                                       hover_color="#54FF9F",
                                       text_color="black",
                                       font=ctk.CTkFont("TkDefaultFont", 16),
                                       command=lambda: self.update_click())
            update_btn.pack(fill=tk.X, expand=0, side="left", padx=5)

            delete_btn = ctk.CTkButton(group_option,
                                       text="Xóa",
                                       corner_radius=18,
                                       border_width=0,
                                       height=36,
                                       fg_color="Firebrick1",
                                       hover_color="#FFC0CB",
                                       text_color="black",
                                       font=ctk.CTkFont("TkDefaultFont", 16),
                                       command=lambda: self.delete_click())
            delete_btn.pack(fill=tk.X, expand=0, side="left")

    def __ui_detail_form(self, main_fr):
        padding_x = 25
        padding_y = 5
        entry_width = 300
        entry_padding_y = 5
        global created_date_entry
        detail_fr = ctk.CTkFrame(main_fr, border_width=2,
                                 fg_color="white",
                                 corner_radius=10, border_color="gray")
        detail_fr.pack(fill=tk.Y, expand=1, padx=20, pady=5)

        detail_lb = ctk.CTkLabel(detail_fr, text="Thông tin chi tiết", text_color="#000088",
                                 font=ctk.CTkFont("TkDefaultFont", 16, 'bold'))
        detail_lb.pack(fill=tk.X, expand=0, padx=20, side="top", pady=5)

        self.sub_fr = ctk.CTkFrame(detail_fr, fg_color="white")
        self.sub_fr.pack(fill=tk.X, expand=0, padx=padding_x, pady=padding_y, ipadx=10)
        self.sub_fr.columnconfigure(0, weight=1)

        self.customer_name_lb = ctk.CTkLabel(self.sub_fr, text="Họ tên khách hàng", anchor=tk.W,
                                             font=ctk.CTkFont("TkDefaultFont", 14, 'bold'))
        self.customer_name_lb.grid(row=0, column=0, sticky=tk.NW)
        customer_name_entry = ctk.CTkEntry(self.sub_fr,
                                           textvariable=self.__customer_name_var,
                                           placeholder_text="Nhập họ tên khách hàng",
                                           width=entry_width)
        customer_name_entry.grid(row=0, column=1, sticky=tk.NW, pady=entry_padding_y)

        customer_phone_lb = ctk.CTkLabel(self.sub_fr, text="Số điện thoại khách hàng", anchor=tk.W,
                                         font=ctk.CTkFont("TkDefaultFont", 14, 'bold'))
        customer_phone_lb.grid(row=1, column=0, sticky=tk.NW)

        customer_phone_entry = ctk.CTkEntry(self.sub_fr,
                                            textvariable=self.__phone_var,
                                            placeholder_text="Nhập số điện thoại",
                                            width=entry_width,
                                            validate="key",
                                            validatecommand=(self._phone_validation, '%S'))
        customer_phone_entry.grid(row=1, column=1, sticky=tk.NW, pady=entry_padding_y)

        created_date_lb = ctk.CTkLabel(self.sub_fr, text="Ngày tạo", anchor=tk.W,
                                       font=ctk.CTkFont("TkDefaultFont", 14, 'bold'))
        created_date_lb.grid(row=2, column=0, sticky=tk.NW)

        created_date_entry = CEntryDate(self.sub_fr, style="success")
        created_date_entry.grid(row=2, column=1, sticky=tk.NW, pady=entry_padding_y)

        bill_type_lb = ctk.CTkLabel(self.sub_fr, text="Loại hóa đơn", anchor=tk.W,
                                    font=ctk.CTkFont("TkDefaultFont", 14, 'bold'))
        bill_type_lb.grid(row=3, column=0, sticky=tk.NW)

        bill_type_cbb_values = list(self.__bill_type_dict.values())
        bill_type_cbb = ctk.CTkComboBox(self.sub_fr,
                                        width=150,
                                        button_color="DodgerBlue2",
                                        variable=self.__bill_type_var,
                                        state="readonly",
                                        values=bill_type_cbb_values)
        bill_type_cbb.grid(row=3, column=1, sticky=tk.NW, pady=entry_padding_y)

        status_lb = ctk.CTkLabel(self.sub_fr, text="Trạng thái", anchor=tk.W,
                                 font=ctk.CTkFont("TkDefaultFont", 14, 'bold'))
        status_lb.grid(row=4, column=0, sticky=tk.NW)
        status_cbb_values = list(self.__status_values.values())
        self.status_cbb = ctk.CTkComboBox(self.sub_fr,
                                          width=150,
                                          button_color="DodgerBlue2",
                                          variable=self.__bill_status_var,
                                          state="readonly",
                                          values=status_cbb_values)
        self.status_cbb.grid(row=4, column=1, sticky=tk.NW, pady=entry_padding_y)
        self.money_lb = ctk.CTkLabel(self.sub_fr, text="Tổng tiền", anchor=tk.W,
                                     font=ctk.CTkFont("TkDefaultFont", 14, 'bold'))
        self.money_lb.grid(row=5, column=0, sticky=tk.NW)
        money_entry = ctk.CTkEntry(self.sub_fr,
                                   textvariable=self.__money_var,
                                   width=entry_width,
                                   placeholder_text="Nhập tổng tiền",
                                   placeholder_text_color="gray",
                                   validate="key",
                                   validatecommand=(self._money_validation, '%S'))
        money_entry.grid(row=5, column=1, sticky=tk.NW, pady=entry_padding_y)
        self.valid_lb = ctk.CTkLabel(master=detail_fr,
                                     text="Vui lòng nhập tổng tiền",
                                     font=ctk.CTkFont("TkDefaultFont", 14),
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
        date_selected = datetime.strptime(date_entry_filter.date_text, "%Y-%m-%d")
        bills = self.__controller.get_data_by_date(by_date=date_selected)
        for item in self.tv.get_children():
            self.tv.delete(item)
        self.__insert_column_values(bill_list=bills)

    def __insert_column_values(self, bill_list=None):
        my_tag = "blue"
        bills = self.__controller.bills
        if bill_list:
            bills = bill_list
        for b in bills:
            if b.type == BillType.REVENUE.value[1]:
                my_tag = "blue"
            else:
                my_tag = "normal"

            # ("id", "user_create", "customer_name", "customer_phone", "table_num", "create_date", "bill_type",
            #     "total_money", "update_date")
            user_name = self.__controller.get_user_name_by_id(b.userId)
            table_num = self.__controller.get_table_num_by_id(b.tableId)
            self.tv.insert("", "end", iid=b.id, text=b.id,
                           values=(b.id, user_name, b.customerName, b.customerPhoneNumber,
                                   table_num, f"{b.createdDate:%Y-%m-%d}",
                                   self.__bill_type_dict.get(b.type), f"{b.totalMoney:0,.0f}",
                                   self.__status_values.get(b.status)),
                           tags=my_tag)

    def add_click(self):
        valid_text = ""
        is_validate = lambda text: 0 if len(text) == 0 or text.isspace() == 1 else 1
        if not is_validate(self.__customer_name_var.get()):
            if len(valid_text) == 0:
                valid_text = f"Vui lòng nhập {self.customer_name_lb.cget('text')}"
            else:
                valid_text = f"{valid_text}, {self.customer_name_lb.cget('text')}"

        if not is_validate(self.__money_var.get()):
            if len(valid_text) == 0:
                valid_text = f"Vui lòng nhập {self.money_lb.cget('text')}"
            else:
                valid_text = f"{valid_text}, {self.money_lb.cget('text')}"

        if valid_text:
            self.show_validate(valid_text)
        else:
            self.__controller.add_new_bill_and_reload(bill_id=self.__bill_id_selected)
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
        self.reset_text_entry()

    def delete_click(self):
        selected_items = self.tv.selection()
        if not selected_items:
            messagebox.showwarning("Thông báo", "Vui lòng chọn dòng muốn xóa.")
            return
        if messagebox.askokcancel(title="Thông báo", message="Bạn có muốn xóa hóa đơn này không?"):
            for item in selected_items:
                item_id = self.tv.item(item, "values")[0]
                self.__controller.delete_and_reload(_id=item_id)
            self.reload_treeview()
            self.reset_text_entry()

    def reset_text_entry(self):
        self.__phone_var.set("")
        self.__customer_name_var.set("")
        self.__money_var.set("")

    def reload_treeview(self):
        for item in self.tv.get_children():
            self.tv.delete(item)
        self.__insert_column_values()

    def get_detail_form_values(self):
        bill_type = BillType.REVENUE.value[0] if self.__bill_type_dict.get(
            BillType.REVENUE.value[0]) == self.__bill_type_var.get() else BillType.EXPANDING.value[0]
        status_bill = 0 if self.__status_values.get(0) == self.__bill_status_var.get() else 1
        return {"customerName": self.__customer_name_var.get(),
                "customerPhoneNumber": self.__phone_var.get(),
                "bill_type": bill_type,
                "totalMoney": self.__money_var.get(),
                "status_bill": status_bill,
                "created_date": created_date_entry.date_text}

    def validate_phone_number_input(self, new_value):
        try:
            if str.isdigit(new_value) and len(new_value) <= 10:
                return True
            else:
                return False
        except ValueError:
            return False

    def validation_money_input(self, text):
        try:
            if text.isdigit():
                return True
            else:
                return False
        except ValueError:
            return False

    def item_treeview_selected(self):
        # self.status_cbb.configure(state="disable")
        selected_items = self.tv.selection()
        for item in selected_items:
            cols = self.tv.item(item, "values")
            self.__bill_id_selected = cols[0]
            self.__customer_name_var.set(cols[2])
            self.__phone_var.set(cols[3])
            created_date_entry.date_text = cols[5]
            self.__bill_type_var.set(cols[6])
            self.__money_var.set(cols[7].replace(",", ""))
            self.__bill_status_var.set(cols[8])
