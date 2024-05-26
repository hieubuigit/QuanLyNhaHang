from datetime import datetime
import tkinter as tk
from tkinter import ttk
import customtkinter
import ttkbootstrap as bt
from customtkinter import *

class BillView:
    def __init__(self, window, controller):

        self.__controller = controller
        self.__date_variable = tk.StringVar()
        self.__date_variable.set(f"{datetime.now():%d/%m/%Y}")
        self.__generate_ui_content(window)

    def __generate_ui_content(self, window):
        customtkinter.set_appearance_mode("light")
        style = ttk.Style()
        style.theme_use('default')
        main_fr = CTkFrame(window)
        main_fr.pack(fill=tk.BOTH, expand=1)

        self.ui_header(main_fr)
        # UI TreeView

        self.t = ttk.Treeview(main_fr)
        self.t.pack(fill=tk.X, expand=0, padx=20, side="top")
        style.configure("Treeview.Heading", background="#007BFF", forceground="white", font=("TkDefaultFont", 18))
        self.t["columns"] = ("id", "user_create", "create_date", "customer_name", "customer_phone", "table_num", "total_money")
        self.t["show"] = "headings"
        self.t.column("id", anchor="center", width=80)
        self.t.column("user_create", anchor="center")
        self.t.column("customer_name", anchor="center")
        self.t.column("customer_phone", anchor="center", width=200)
        self.t.column("table_num", anchor="center", width=100)
        self.t.column("total_money", anchor="center")
        self.t.column("create_date", anchor="center", width=200)

        self.t.heading("id", text="ID")
        self.t.heading("user_create", text="Người Tạo")
        self.t.heading("create_date", text="Ngày Tạo")
        self.t.heading("customer_name", text="Tên Khách Hàng")
        self.t.heading("customer_phone", text="SDT Khách Hàng")
        self.t.heading("table_num", text="Số Bàn")
        self.t.heading("total_money", text="Tổng Tền")
        self.t.tag_configure("normal", background="white")
        self.t.tag_configure("blue", background="lightblue")

        # Fill data vào treeview
        self.__insert_column_values()

        self.__ui_detail_form(main_fr)

    def ui_header(self, main_fr):
        option_fr = CTkFrame(main_fr, fg_color="transparent")
        option_fr.pack(fill=tk.X, expand=0, pady=10, padx=20)
        lb_date = CTkLabel(option_fr, text="Ngày tạo")
        lb_date.pack(fill=tk.X, expand=0, side="left", padx=5)

        date_entry = bt.DateEntry(option_fr, dateformat="%d/%m/%Y", bootstyle="primary")
        date_entry.entry.configure(textvariable=self.__date_variable)
        self.__date_variable.trace('w', lambda name, index, mode, date_value=self.__date_variable: self.change_date_reload_view())
        date_entry.pack(side="left")

        group_option = CTkFrame(option_fr, fg_color="green")
        add_btn = CTkButton(group_option, text="Thêm mới", corner_radius=4, border_width=0,
                            command=lambda: self.add_click())
        add_btn.pack(fill=tk.X, expand=0, side="left")

        update_btn = CTkButton(group_option, text="Chỉnh sửa", corner_radius=4, border_width=0,
                               command=lambda: self.update_click())
        update_btn.pack(fill=tk.X, expand=0, side="left")

        delete_btn = CTkButton(group_option, text="Xóa", corner_radius=4, border_width=0,
                               command=lambda: self.delete_click())
        delete_btn.pack(fill=tk.X, expand=0, side="left")
        group_option.pack(side="right")

    def __ui_detail_form(self, main_fr):
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

        sub_fr = CTkFrame(detail_fr, fg_color="white")
        sub_fr.pack(fill=tk.BOTH, expand=1, padx=padding_x, pady=padding_y, ipadx=10)

        sub_fr.grid_columnconfigure(0, weight=1)

        creator_name_lb = CTkLabel(sub_fr, text="Tên người tạo:",
                                   font=CTkFont("TkDefaultFont", 14, 'bold'),
                                   anchor=tk.W)
        creator_name_lb.grid(row=0, column=0, sticky=tk.NW)
        creator_name_entry = CTkEntry(sub_fr, placeholder_text="Nhập họ tên người tạo", width=entry_width)
        creator_name_entry.grid(row=0, column=1, sticky=(tk.N, tk.W), pady=entry_padding_y)
        creator_name_valid_lb = CTkLabel(master=sub_fr,
                                         text="Vui lòng nhập họ tên người tạo",
                                         font=CTkFont("TkDefaultFont", 14),
                                         text_color="red",
                                         anchor=tk.W)
        creator_name_valid_lb.grid(row=1, column=1, sticky=tk.NW)

        customer_name_lb = CTkLabel(sub_fr, text="Họ tên khách hàng", anchor=tk.W,
                                    font=CTkFont("TkDefaultFont", 14, 'bold'))
        customer_name_lb.grid(row=2, column=0, sticky=tk.NW)
        customer_name_entry = CTkEntry(sub_fr, placeholder_text="Nhập họ tên khách hàng", width=entry_width)
        customer_name_entry.grid(row=2, column=1, sticky=tk.NW, pady=entry_padding_y)
        customer_name_valid_lb = CTkLabel(master=sub_fr,
                                          text="Vui lòng nhập họ tên khách hàng",
                                          font=CTkFont("TkDefaultFont", 14),
                                          text_color="red",
                                          anchor=tk.W)
        customer_name_valid_lb.grid(row=3, column=1, sticky=tk.NW)

        customer_phone_lb = CTkLabel(sub_fr, text="Số điện thoại khách hàng", anchor=tk.W,
                                     font=CTkFont("TkDefaultFont", 14, 'bold'))
        customer_phone_lb.grid(row=4, column=0, sticky=tk.NW)
        customer_phone_entry = CTkEntry(sub_fr, placeholder_text="Nhập số điện thoại", width=entry_width)
        customer_phone_entry.grid(row=4, column=1, sticky=tk.NW, pady=entry_padding_y)
        phone_valid_lb = CTkLabel(master=sub_fr,
                                  text="Số điện thoại không đúng định dạng",
                                  font=CTkFont("TkDefaultFont", 14),
                                  text_color="red",
                                  anchor=tk.W)
        phone_valid_lb.grid(row=5, column=1, sticky=tk.NW)

        created_date_lb = CTkLabel(sub_fr, text="Ngày tạo", anchor=tk.W,
                                   font=CTkFont("TkDefaultFont", 14, 'bold'))
        created_date_lb.grid(row=6, column=0, sticky=tk.NW)
        created_date_entry = bt.DateEntry(sub_fr, dateformat="%d/%m/%Y", bootstyle="primary")
        created_date_entry.grid(row=6, column=1, sticky=tk.NW, pady=entry_padding_y)

        table_lb = CTkLabel(sub_fr, text="Số bàn", anchor=tk.W, font=CTkFont("TkDefaultFont", 14, 'bold'))
        table_lb.grid(row=7, column=0, sticky=tk.NW)
        table_entry = CTkEntry(sub_fr, placeholder_text="Nhập số bàn", width=150)
        table_entry.grid(row=7, column=1, sticky=tk.NW, pady=entry_padding_y)

        money_lb = CTkLabel(sub_fr, text="Tổng tiền", anchor=tk.W,
                            font=CTkFont("TkDefaultFont", 14, 'bold'))
        money_lb.grid(row=8, column=0, sticky=tk.NW)
        money_entry = CTkEntry(sub_fr,
                               width=entry_width,
                               placeholder_text="Nhập tổng tiền")
        money_entry.grid(row=8, column=1, sticky=tk.NW, pady=entry_padding_y)
        money_valid_lb = CTkLabel(master=sub_fr,
                                  text="Vui lòng nhập tổng tiền",
                                  font=CTkFont("TkDefaultFont", 14),
                                  text_color="red",
                                  anchor=tk.W)
        money_valid_lb.grid(row=9, column=1, sticky=tk.NW)



    def change_date_reload_view(self):
        for item in self.t.get_children():
            self.t.delete(item)
        if self.__date_variable.get() != '':
            self.__insert_column_values(datetime.strptime(self.__date_variable.get(), "%d/%m/%Y"))

    def __insert_column_values(self, by_date=datetime.now()):
        my_tag = "blue"
        bills = self.__controller.get_data(by_date)
        for bill in bills:
            if my_tag == "normal":
                my_tag = "blue"
            else:
                my_tag = "normal"
            self.t.insert("", "end", iid=bill.id, text=bill.id,
                          values=(bill.id, bill.userId, bill.createdDate, bill.customerName, bill.customerPhoneNumber,
                                  bill.tableId, bill.totalMoney),
                          tags=my_tag)

    def add_click(self):
        pass
        # if self.__current_page == StatePage.Product:
        #     img = base64.b64encode(self.thumbnail_bytes)
        #     self.__controller.add_new_and_reload(name=self.product_name_var.get(),
        #                                          price=self.product_price_var.get(),
        #                                          unit=self.product_unit_var.get(),
        #                                          quantity=self.product_quantity_var.get(),
        #                                          capacity=self.product_capacity_var.get(),
        #                                          alcohol=self.product_alcohol_var.get(),
        #                                          productType=self.product_type_var.get(),
        #                                          image=img)
        #     self.reload_treeview()
        # else:
        #     self.__controller.add_discount()


    def update_click(self):
        pass
        # if self.__current_page == StatePage.Product:
        #     selected_items = self.tv.selection()
        #     if not selected_items:
        #         messagebox.showwarning("Thông báo", "Vui lòng chọn dòng muốn chỉnh sửa.")
        #         return
        #     img = base64.b64encode(self.thumbnail_bytes)
        #     for item in selected_items:
        #         item_id = self.tv.item(item, "values")[0]
        #         self.__controller.update_and_reload(id=item_id,
        #                                             name=self.product_name_var.get(),
        #                                             price=self.product_price_var.get(),
        #                                             unit=self.product_unit_var.get(),
        #                                             quantity=self.product_quantity_var.get(),
        #                                             capacity=self.product_capacity_var.get(),
        #                                             alcohol=self.product_alcohol_var.get(),
        #                                             product_type=self.product_type_var.get(),
        #                                             image=img)
        #     self.reload_treeview()
        # else:
        #     self.__controller.update_row_discount()


    def delete_click(self):
        pass
        # if self.__current_page == StatePage.Product:
        #     selected_items = self.tv.selection()
        #     if not selected_items:
        #         messagebox.showwarning("Thông báo", "Vui lòng chọn dòng muốn xóa.")
        #         return
        #     if messagebox.askokcancel(title="Thông báo", message="Bạn có chắc chắn muốn xóa sản phẩm này không?"):
        #         for item in selected_items:
        #             item_id = self.tv.item(item, "values")[0]
        #             self.tv.delete(item)
        #             self.__controller.delete_and_reload(id=item_id)
        #         self.reload_treeview()
        # else:
        #     self.__controller.delete_row_discount()

