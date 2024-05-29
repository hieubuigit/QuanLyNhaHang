import tkinter as tk
from datetime import datetime
from tkinter import ttk

import customtkinter
from PIL import Image, ImageTk
from customtkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReportView:
    def __init__(self, window, controller):
        customtkinter.set_appearance_mode("light")
        self.__controller = controller
        self.__quarter_var = tk.StringVar()
        self.__ui_main_content(window)

    def __ui_main_content(self, root):
        style = ttk.Style()
        style.theme_use('default')
        main_fr = CTkFrame(root)
        main_fr.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.__ui_left_view(root, main_fr)
        self.sub_fr = CTkFrame(main_fr, border_width=1, border_color="gray")
        self.sub_fr.pack(fill=tk.BOTH, expand=1)

        # default right content
        self.__report_page()

    def __ui_left_view(self, root, main_fr):
        style = ttk.Style()
        style.theme_use('default')
        left_fr = CTkFrame(main_fr, border_width=1, border_color="gray")
        left_fr.pack(fill=tk.Y, expand=0, side="left", anchor="nw", padx=1, pady=1, ipadx=2)

        btn_gr = CTkFrame(left_fr)
        btn_gr.pack(pady=3)
        ic_revenue = CTkImage(Image.open("../assets/profits.png"), size=(25, 25))
        self.revenue_btn = CTkButton(btn_gr,
                                     text="Doanh thu",
                                     width=150,
                                     height=30,
                                     corner_radius=1,
                                     image=ic_revenue,
                                     compound=tk.LEFT,
                                     fg_color="white",
                                     text_color="DodgerBlue1",
                                     hover_color="#63B8FF",
                                     anchor=tk.W,
                                     command=lambda: self.__switch_page(root, main_fr, page="REVENUE"))
        self.revenue_btn.grid(row=0, column=0)
        self.revenue_line = CTkFrame(btn_gr, fg_color="DodgerBlue1", height=30, width=2, corner_radius=0,
                                     border_width=0)
        self.revenue_line.grid(row=0, column=1)

        ic_salary = CTkImage(Image.open("../assets/revenue.png"), size=(25, 25))
        self.salary_btn = CTkButton(btn_gr,
                                    text="Lương nhân viên",
                                    width=150,
                                    height=30,
                                    corner_radius=1,
                                    image=ic_salary,
                                    compound=tk.LEFT,
                                    fg_color="white",
                                    text_color="black",
                                    hover_color="#63B8FF",
                                    anchor=tk.W,
                                    command=lambda: self.__switch_page(root, main_fr, page="SALARY"))
        self.salary_btn.grid(row=1, column=0)
        self.salary_line = CTkFrame(btn_gr, fg_color="white", height=30, width=2, corner_radius=0,
                                    border_width=0)
        self.salary_line.grid(row=1, column=1)

    def ui_right_content_view(self):
        padding = 2
        header_fr = CTkFrame(self.sub_fr, corner_radius=0)
        header_fr.pack(fill=tk.X, expand=0, padx=padding, pady=padding)
        header_fr.columnconfigure(0, weight=1)
        quarters = {1: "Quý 1", 2: "Quý 2", 3: "Quý 3", 4: "Quý 4"}
        quarters_values = list(quarters.values())
        ic_filter = CTkImage(Image.open("../assets/funnel.png"), size=(25, 25))
        filter_btn = CTkButton(header_fr, text="", image=ic_filter, width=50,
                               fg_color="white", border_width=1, hover_color="#63B8FF",
                               command=lambda:self.quarter_button_callback())
        filter_btn.pack(fill=tk.BOTH, expand=0, side=tk.RIGHT, anchor=tk.E, padx=3)

        filter_cbb = CTkComboBox(header_fr, values=quarters_values,
                                 state="readonly",
                                 variable=self.__quarter_var)

        filter_cbb.pack(fill=tk.BOTH, expand=0, side=tk.RIGHT, anchor=tk.E)

        chart_fr = CTkFrame(self.sub_fr, corner_radius=0)
        chart_fr.pack(fill=tk.BOTH, expand=1, padx=padding, pady=padding)

        left_fr = CTkFrame(chart_fr, corner_radius=0, border_width=1, border_color="gray", fg_color="white")
        left_fr.grid(row=0, column=0)

        self.open_pie_chart(left_fr)
        chart_fr.grid_columnconfigure(0, weight=1)
        right_fr = CTkFrame(chart_fr, corner_radius=0, border_width=1, border_color="gray")

        right_fr.grid(row=0, column=1)
        self.open_bar_chart(right_fr)
        chart_fr.grid_columnconfigure(1, weight=1)

        # Tạo UI Treeview load thông tin hóa đơn
        self.create_ui_buttom()

    def create_ui_buttom(self):
        padding = 2
        bottom_fr = CTkFrame(self.sub_fr)
        bottom_fr.pack(fill=tk.BOTH, expand=1, padx=padding)
        # UI TreeView
        style = ttk.Style()
        style.theme_use('default')
        tree_scrollX = customtkinter.CTkScrollbar(bottom_fr, height=15)
        tree_scrollX.pack(side=tk.BOTTOM, fill='x')
        self.tv = ttk.Treeview(bottom_fr, yscrollcommand=tree_scrollX.set)
        self.tv.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
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
    def __switch_page(self, root, main_fr, page):
        for fr in self.sub_fr.winfo_children():
            fr.destroy()
            root.update()
        if page == "SALARY":
            self.salary_page(main_fr)
            self.salary_line.configure(fg_color="DodgerBlue1")
            self.salary_btn.configure(text_color="DodgerBlue1")
            self.revenue_line.configure(fg_color="white")
            self.revenue_btn.configure(text_color="black")
        else:
            self.__report_page()
            self.revenue_line.configure(fg_color="DodgerBlue1")
            self.revenue_btn.configure(text_color="DodgerBlue1")
            self.salary_line.configure(fg_color="white")
            self.salary_btn.configure(text_color="black")

    def data_example(self):
        bills = (200, 300)
        return bills

    def open_pie_chart(self, main_fr):
        data = self.data_example()
        input_text = [data.__getitem__(0), data.__getitem__(1)]
        vehicles = ['Tổng Thu', 'Tổng Chi']
        fig = plt.Figure(figsize=(5, 3.7), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(input_text, radius=1, labels=vehicles, colors=["#009900", "#FF6633"])
        chart = FigureCanvasTkAgg(fig, main_fr)
        chart.get_tk_widget().pack(side="top", fill='both', expand=True, padx=1, pady=1)
        note_fr = CTkFrame(main_fr, corner_radius=0)
        note_fr.pack(fill=tk.X, expand=0)
        total_revenue_title = CTkButton(note_fr, text=str(data.__getitem__(0)), fg_color="#009900",
                                        text_color="black",
                                        border_width=1, state="disable", corner_radius=0)
        total_revenue_title.grid(row=0, column=0)
        total_spending_title = CTkButton(note_fr, text=str(data.__getitem__(1)),
                                         fg_color="#FF6633",
                                         text_color="black",
                                         border_width=1, state="disable", corner_radius=0)
        total_spending_title.grid(row=0, column=1)

    def open_bar_chart(self, main_fr):
        f = plt.Figure(figsize=(5, 4), dpi=100)
        ax = f.add_subplot(111)
        data = (20, 35, 30)
        # ind_quarter = quarters[0].get(1)
        # print(ind_quarter)
        # start_range_quarter = ind_quarter * 2
        # end_range_quarter = start_range_quarter + 3
        ind = [x for x in range(1, 4)]
        width = .5
        ind_str = [f"Tháng {x}" for x in range(1, 4)]
        ax.bar(ind, data, width, tick_label=ind_str)
        canvas = FigureCanvasTkAgg(f, master=main_fr)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    def __report_page(self):
        self.ui_right_content_view()

    def salary_page(self, main_fr):
        # add employee frame
        salary_fr = ttk.Frame(self.sub_fr)
        lb = ttk.Label(salary_fr, text="Salary Page")
        lb.pack()
        salary_fr.pack()

    def quarter_button_callback(self):
        print(self.__quarter_var.get())

    def __insert_column_values(self):
        my_tag = "blue"
        bills = self.__controller.get_bills()
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

    def change_date_reload_view(self):
        pass
        # if self.__date_variable.get() != '':
        #     for item in self.tv.get_children():
        #         self.tv.delete(item)
        #     self.__insert_column_values(datetime.strptime(self.__date_variable.get(), "%d/%m/%Y"))

