import math
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import numpy as np
from PIL import Image
from customtkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pay_grade.pay_grade_view import PayGradeView
from payslip.pay_slip_view import PaySlipView
from share.common_config import BillType, ReportTab, BillStatus

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ReportView:
    def __init__(self, window, controller):
        self.__controller = controller
        self.__quarters = {1: "Quý 1", 2: "Quý 2", 3: "Quý 3", 4: "Quý 4"}
        self.__quarter_var = tk.StringVar()
        self._status_values = {BillStatus.PAID.value: "Đã thanh toán", BillStatus.UNPAID.value: "Chưa thanh toán"}

        self.__ui_main_content(window)

    def __ui_main_content(self, root):
        main_fr = CTkFrame(root)
        main_fr.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.__ui_left_view(root, main_fr)
        self.sub_fr = CTkFrame(main_fr, border_width=1, border_color="gray")
        self.sub_fr.pack(fill=tk.BOTH, expand=1)

        # default right content
        self.__report_page()

    def __ui_left_view(self, root, main_fr):
        left_fr = CTkFrame(main_fr, border_width=1, border_color="gray", fg_color="white")
        left_fr.pack(fill=tk.Y, expand=0, side="left", anchor="nw", padx=(2, 10), pady=1, ipadx=2)

        btn_gr = CTkFrame(left_fr)
        btn_gr.pack(pady=3)

        # Revenue tab
        ic_revenue = CTkImage(Image.open("../assets/profits.png"), size=(25, 25))
        self.revenue_btn = CTkButton(btn_gr,
                                     text="Doanh thu",
                                     width=150,
                                     height=30,
                                     corner_radius=1,
                                     image=ic_revenue,
                                     compound=tk.LEFT,
                                     fg_color="white",
                                     text_color="#000080",
                                     hover_color="#63B8FF",
                                     anchor=tk.W,
                                     command=lambda: self.__switch_page(root, main_fr, page=ReportTab.REVENUE))
        self.revenue_btn.grid(row=0, column=0)
        self.revenue_line = CTkFrame(btn_gr, fg_color="#000080", height=30, width=2, corner_radius=0,
                                     border_width=0)
        self.revenue_line.grid(row=0, column=1)

        # Employee salary tab
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
                                    command=lambda: self.__switch_page(root, main_fr, page=ReportTab.SALARY))
        self.salary_btn.grid(row=1, column=0)
        self.salary_line = CTkFrame(btn_gr, fg_color="white", height=30, width=2, corner_radius=0,
                                    border_width=0)
        self.salary_line.grid(row=1, column=1)

        # Employee salary tab
        salary_grade_img = CTkImage(Image.open("../assets/star.png"), size=(25, 25))
        self.salary_grade_btn = CTkButton(btn_gr,
                                          text="Bậc lương",
                                          width=150,
                                          height=30,
                                          corner_radius=1,
                                          image=salary_grade_img,
                                          compound=tk.LEFT,
                                          fg_color="white",
                                          text_color="black",
                                          hover_color="#63B8FF",
                                          anchor=tk.W,
                                          command=lambda: self.__switch_page(root, main_fr,
                                                                             page=ReportTab.SALARY_GRADE))
        self.salary_grade_btn.grid(row=2, column=0)
        self.salary_grade_line = CTkFrame(btn_gr, fg_color="white", height=30, width=2, corner_radius=0, border_width=0)
        self.salary_grade_line.grid(row=2, column=1)

    def ui_right_content_view(self):
        global pie_chart_fr, bar_chart_fr
        padding = 2
        header_fr = CTkFrame(self.sub_fr, corner_radius=0, fg_color="white")
        header_fr.pack(fill=tk.X, expand=0, padx=padding, pady=(2, 0))
        header_fr.columnconfigure(0, weight=1)
        quarters_values = list(self.__quarters.values())
        current_quarter_key = self.__controller.current_quarter
        self.__quarter_var.set(self.__quarters.get(current_quarter_key))
        ic_filter = CTkImage(Image.open("../assets/funnel.png"), size=(25, 25))
        filter_btn = CTkButton(header_fr, text="", image=ic_filter, width=50,
                               fg_color="white", border_width=1, hover_color="#63B8FF",
                               command=lambda: self.quarter_button_callback())
        filter_btn.pack(fill=tk.BOTH, expand=0, side=tk.RIGHT, anchor=tk.E, padx=3)

        filter_cbb = CTkComboBox(header_fr,
                                 values=quarters_values,
                                 state="readonly",
                                 variable=self.__quarter_var)
        filter_cbb.pack(fill=tk.BOTH, expand=0, side=tk.RIGHT, anchor=tk.E)

        chart_fr = CTkFrame(self.sub_fr, corner_radius=0)
        chart_fr.pack(fill=tk.BOTH, expand=1, padx=padding, pady=(2, 0))

        pie_chart_fr = CTkFrame(chart_fr, corner_radius=0, border_width=1, border_color="gray", fg_color="white")
        pie_chart_fr.grid(row=0, column=0)

        self.open_pie_chart(pie_chart_fr)
        chart_fr.grid_columnconfigure(0, weight=1)

        bar_chart_fr = CTkFrame(chart_fr, corner_radius=0, border_width=1, border_color="gray")
        bar_chart_fr.grid(row=0, column=1)
        self.open_bar_chart(bar_chart_fr)
        chart_fr.grid_columnconfigure(1, weight=1)

        # Tạo UI Treeview load thông tin hóa đơn
        self.create_ui_bottom_view()

    def create_ui_bottom_view(self):
        padding = 2
        bottom_fr = CTkFrame(self.sub_fr, corner_radius=0)
        bottom_fr.pack(fill=tk.BOTH, expand=1, padx=padding, pady=2)
        # UI TreeView
        style = ttk.Style()
        style.theme_use('default')

        self.tv = ttk.Treeview(bottom_fr)
        self.tv.pack(fill=tk.BOTH, expand=1, padx=10, pady=3)
        style.configure("Treeview.Heading", background="DodgerBlue1", forceground="white", font=("TkDefaultFont", 18))
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
        tree_scrollX = CTkScrollbar(bottom_fr, height=15, orientation=tk.HORIZONTAL, command=self.tv.xview)
        tree_scrollX.pack(side=tk.BOTTOM, fill='x')
        self.tv.configure(xscrollcommand=tree_scrollX.set)
        # Fill data vào treeview
        self.__insert_column_values()

    def __switch_page(self, root, main_fr, page: ReportTab):
        for fr in self.sub_fr.winfo_children():
            fr.destroy()
            root.update()
        if page == ReportTab.REVENUE:
            self.__report_page()
            self.salary_line.configure(fg_color="white")
            self.salary_btn.configure(text_color="black")
            self.revenue_line.configure(fg_color="#000080")
            self.revenue_btn.configure(text_color="#000080")
            self.salary_grade_btn.configure(text_color="black")
            self.salary_grade_line.configure(fg_color="white")

        elif page == ReportTab.SALARY:
            self.salary_page(main_fr)
            self.salary_line.configure(fg_color="#000080")
            self.salary_btn.configure(text_color="#000080")
            self.revenue_line.configure(fg_color="white")
            self.revenue_btn.configure(text_color="black")
            self.salary_grade_btn.configure(text_color="black")
            self.salary_grade_line.configure(fg_color="white")
        elif page == ReportTab.SALARY_GRADE:
            self.salary_grade_page(main_fr)
            self.salary_line.configure(fg_color="white")
            self.salary_btn.configure(text_color="black")
            self.revenue_line.configure(fg_color="white")
            self.revenue_btn.configure(text_color="black")
            self.salary_grade_btn.configure(text_color="#000080")
            self.salary_grade_line.configure(fg_color="#000080")

    def open_pie_chart(self, main_fr):
        input_text = [self.__controller.total_revenue, self.__controller.total_expend]
        vehicles = ["Tổng Thu", "Tổng Chi"]
        if self.__controller.total_expend > 0 or self.__controller.total_revenue > 0:
            fig = plt.Figure(figsize=(5, 3.7), dpi=100)
            ax = fig.add_subplot(111)
            ax.pie(input_text, radius=1, labels=vehicles, colors=["#009900", "#FF6633"])
            chart = FigureCanvasTkAgg(fig, main_fr)
            chart.get_tk_widget().pack(side="top", fill='both', expand=True, padx=1, pady=1)
            note_fr = CTkFrame(main_fr, corner_radius=0)
            note_fr.pack(fill=tk.X, expand=0)
            total_revenue_value = f"{self.__controller.total_revenue:0,.0f} VND"
            total_expand_value = f"{self.__controller.total_expend:0,.0f} VND"

            total_revenue_title = CTkButton(note_fr, text=total_revenue_value, fg_color="#009900",
                                            text_color="black",
                                            border_width=1, state="disable", corner_radius=0)
            total_revenue_title.grid(row=0, column=0)
            total_spending_title = CTkButton(note_fr, text=total_expand_value,
                                             fg_color="#FF6633",
                                             text_color="black",
                                             border_width=1, state="disable", corner_radius=0)
            total_spending_title.grid(row=0, column=1)
        else:
            fig = plt.Figure(figsize=(6, 4), dpi=100)
            ax = fig.text(x=0.35, y=0.5, s="Không có dữ liệu")
            empty_fr = FigureCanvasTkAgg(fig, main_fr)
            empty_fr.draw()
            empty_fr.get_tk_widget().pack(side="top", fill='both', expand=True, padx=1, pady=1)

    def open_bar_chart(self, main_fr):
        f = plt.Figure(figsize=(6, 4), dpi=100)
        ax = f.add_subplot(111)
        ax.set_ylabel('Đơn vị: Triệu')
        bills = self.__controller.bills
        ind_month = self.__controller.months_of_the_quarter
        width = .4
        r = np.arange(3)
        expend_value_by_month = []
        revenue_value_by_month = []
        max_value = 50
        if ind_month:
            for m in ind_month:
                revenue_total = sum(i.totalMoney for i in bills if i.type == BillType.REVENUE.value[0]
                                    and i.createdDate.month == m) / 1000000
                revenue_value_by_month.append(revenue_total)
                expend_total = sum(i.totalMoney for i in bills if i.type == BillType.EXPANDING.value[0]
                                   and i.createdDate.month == m) / 1000000
                expend_value_by_month.append(expend_total)
            expand_max_value = float(max(expend_value_by_month, key=lambda x: float(x)))
            revenue_max_value = float(max(revenue_value_by_month, key=lambda x: float(x)))
            max_value = expand_max_value if expand_max_value > revenue_max_value else revenue_max_value
            if max_value < 1:
                max_value = 10
            step = math.ceil(max_value / 5)
            ticks_loc = np.arange(0, max_value, step=step)
            ind_str = [f"Tháng {x}" for x in ind_month]
            ax.bar(r - 0.2, revenue_value_by_month, width, label='Thu')
            ax.bar(r + 0.2, expend_value_by_month, width, label="Chi")
            ax.set_xticks(r, ind_str)
            ax.set_yticks(ticks_loc)
            ax.legend()
        canvas = FigureCanvasTkAgg(f, master=main_fr)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    def __report_page(self):
        self.ui_right_content_view()

    def salary_grade_page(self, main_fr):
        salary_grade_fr = ctk.CTkFrame(self.sub_fr)
        pay_grade = PayGradeView(salary_grade_fr)
        salary_grade_fr.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor='nw')

    def salary_page(self, main_fr):
        salary_fr = ctk.CTkFrame(self.sub_fr)
        payslip = PaySlipView(salary_fr)
        salary_fr.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor='nw')

    def quarter_button_callback(self):
        value_key_dict = {value: key for key, value in self.__quarters.items()}
        searched_key = value_key_dict[self.__quarter_var.get()]
        self.__controller.get_bills_and_reload_view(searched_key)
        self.reload_pie_chart_view(pie_chart_fr)
        self.reload_bar_chart_view(bar_chart_fr)

    def __insert_column_values(self):
        my_tag = "blue"
        bills = self.__controller.bills
        for b in bills:
            if my_tag == "normal":
                my_tag = "blue"
            else:
                my_tag = "normal"
            # ("id", "user_create", "customer_name", "customer_phone", "table_num", "create_date", "bill_type",
            #     "total_money", "update_date")
            user_name = self.__controller.get_user_name_by_id(b.userId)
            table_num = self.__controller.get_table_num_by_id(b.tableId)
            bill_type = BillType.REVENUE.value[1] if b.type == 0 else BillType.EXPANDING.value[1]
            self.tv.insert("", "end", iid=b.id, text=b.id,
                           values=(b.id, user_name, b.customerName, b.customerPhoneNumber,
                                   table_num, f"{b.createdDate:%Y-%m-%d}", bill_type, f"{b.totalMoney:0,.0f}",
                                   self._status_values.get(b.status)),
                           tags=my_tag)

    def reload_treeview(self):
        for item in self.tv.get_children():
            self.tv.delete(item)
        self.__insert_column_values()

    def reload_pie_chart_view(self, main_fr):
        for child in main_fr.winfo_children():
            child.destroy()
        self.open_pie_chart(main_fr)

    def reload_bar_chart_view(self, main_fr):
        for child in main_fr.winfo_children():
            child.destroy()
        self.open_bar_chart(main_fr)
