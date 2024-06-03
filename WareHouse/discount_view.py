import tkinter as tk
from datetime import datetime
from tkinter import ttk
import customtkinter
from customtkinter import *
from share.CEntryDate import CEntryDate


class DiscountView:
    def __init__(self, root, controller):
        self._controller = controller
        self._description_var = tk.StringVar()
        self._percent_var = tk.StringVar()
        self._quantity_var = tk.StringVar()
        self._start_date_var = tk.StringVar()
        self._end_date_var = tk.StringVar()
        self._id_selected = None
        self.create_ui_view(root)

    @property
    def id_selected(self):
        return self._id_selected

    @id_selected.setter
    def id_selected(self, value):
        self._id_selected = value
    def create_ui_view(self, root):
        customtkinter.set_appearance_mode("light")
        style = ttk.Style()
        style.theme_use('default')
        main_fr = CTkFrame(root, border_width=1, border_color="gray")
        main_fr.pack(fill=tk.BOTH, expand=1)
        self.tv = ttk.Treeview(main_fr)
        self.tv.pack(fill=tk.X, expand=0, padx=10, pady=5)

        style.configure("Treeview.Heading", background="DodgerBlue1", forceground="white", font=("TkDefaultFont", 18))
        self.tv["columns"] = ("id", "description", "percent", "start_date", "end_date", "quantity",
                              "create_date")
        self.tv["show"] = "headings"
        self.tv.column("id", anchor="center", width=50)
        self.tv.column("description", anchor="center")
        self.tv.column("percent", anchor="center", width=80)
        self.tv.column("start_date", anchor="center", width=100)
        self.tv.column("end_date", anchor="center", width=100)
        self.tv.column("quantity", anchor="center", width=100)
        self.tv.column("create_date", anchor="center", width=100)

        self.tv.heading("id", text="ID")
        self.tv.heading("description", text="Nội dung")
        self.tv.heading("percent", text="Phần trăm")
        self.tv.heading("start_date", text="Ngày bắt đầu")
        self.tv.heading("end_date", text="Ngày kết thúc")
        self.tv.heading("quantity", text="Số lượng")
        self.tv.heading("create_date", text="Ngày tạo")
        self.tv.tag_configure("normal", background="white")
        self.tv.tag_configure("blue", background="lightblue")
        self.insert_row_treeview()
        self.tv.bind("<<TreeviewSelect>>", lambda e: self.item_treeview_selected())

        # setup ui detail form
        self.ui_detail_form(main_fr)

    def ui_detail_form(self, main_fr):
        global start_date_entry, end_date_entry
        padding_x = 25
        padding_y = 5
        entry_width = 200

        line = CTkFrame(main_fr, height=2, corner_radius=0, border_width=0)
        line.pack(fill=tk.X, expand=0)

        option_fr = CTkFrame(main_fr, corner_radius=10, fg_color="white")
        option_fr.pack(expand=0, pady=10)

        heading2 = CTkFont("TkDefaultFont", 16, 'bold')

        detail_lb = CTkLabel(option_fr, text="Thông tin chi tiết", text_color="#000088",
                             font=heading2)
        detail_lb.pack(fill=tk.X, expand=0, padx=20, side="top", pady=5)
        self.sub_fr = CTkFrame(option_fr, corner_radius=0)
        self.sub_fr.pack(fill=tk.BOTH, expand=1, padx=padding_x, pady=20, ipadx=10)
        self.sub_fr.columnconfigure(0, weight=1)
        self.sub_fr.rowconfigure(0, weight=1)

        desc_lb = CTkLabel(self.sub_fr, text="Nội dung")
        desc_lb.grid(row=0, column=0, sticky=tk.NW + tk.S)

        desc_entry = CTkEntry(self.sub_fr, width=entry_width, textvariable=self._description_var,
                              corner_radius=0, border_width=1)
        desc_entry.grid(row=0, column=1, sticky=tk.NW)

        quantity_lb = CTkLabel(self.sub_fr, text="Số lượng")
        quantity_lb.grid(row=1, column=0, sticky=tk.NW + tk.S)

        quantity_entry = CTkEntry(self.sub_fr, entry_width,
                                  textvariable=self._quantity_var,
                                  corner_radius=0,
                                  border_width=1)
        quantity_entry.grid(row=1, column=1, sticky=tk.NW + tk.S, pady=padding_y)

        percent_lb = CTkLabel(self.sub_fr, text="Khuyến mãi (%)")
        percent_lb.grid(row=2, column=0, sticky=tk.NW + tk.S)
        percent_cbb = CTkComboBox(self.sub_fr,
                                  corner_radius=1,
                                  border_width=1,
                                  button_color="DodgerBlue2",
                                  values=["5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"],
                                  state="readonly",
                                  variable=self._percent_var)
        percent_cbb.grid(row=2, column=1, sticky=tk.NW + tk.S, pady=3)

        start_date_lb = CTkLabel(self.sub_fr, text="Ngày bắt đầu")
        start_date_lb.grid(row=3, column=0, sticky=tk.NW + tk.S, pady=padding_y)

        start_date_entry = CEntryDate(self.sub_fr, style="success")
        start_date_entry.grid(row=3, column=1, sticky=tk.W)

        end_date_lb = CTkLabel(self.sub_fr, text="Ngày kết thúc")
        end_date_lb.grid(row=4, column=0, sticky=tk.NW + tk.S)

        end_date_entry = CEntryDate(self.sub_fr, style="danger")
        end_date_entry.grid(row=4, column=1, sticky=tk.W)

    def insert_row_treeview(self):
        pass
        discounts = self._controller.discounts
        if discounts:
            for d in discounts:
                # ("id", "description", "percent", "start_date", "end_date", "quantity",
                # "create_date", "update_date")
                self.tv.insert("", "end", iid=d.id, text=d.id,
                               values=(d.id, d.description, f"{d.percent:.0f}", d.start_date, d.end_date,
                                       d.quantity, f"{d.created_date:%Y-%m-%d}"))

    def item_treeview_selected(self):
        selected_items = self.tv.selection()
        for item in selected_items:
            cols = self.tv.item(item, "values")
            self.id_selected = cols[0]
            self._description_var.set(cols[1])
            self._percent_var.set(cols[2])
            start_date_entry.date_text = cols[3]
            end_date_entry.date_text = cols[4]
            self._quantity_var.set(cols[5])

    def reload_treeview(self):
        for item in self.tv.get_children():
            self.tv.delete(item)
        self.insert_row_treeview()

    def get_detail_values(self):
        return {"description": self._description_var.get(), "percent": self._percent_var.get(),
                "quantity": self._quantity_var.get(), "start_date": start_date_entry.date_text,
                "end_date": end_date_entry.date_text}
