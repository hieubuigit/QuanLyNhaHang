

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
class WareHouseView:
    def __init__(self, window):
        self.__ui_main_content(window)
    def __ui_main_content(self, root):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("BG.TFrame", background="#7AC5CD")
        main_fr = ttk.Frame(root, style="BG.TFrame")
        main_fr.pack(fill="both", expand=True)

        header_fr = ttk.Frame(main_fr)
        header_fr.pack(fill=tk.X, expand=0)
        option_group_fr = ttk.Frame(header_fr, borderwidth=1, border=1, relief=tk.RIDGE)
        option_group_fr.pack(fill=tk.X, expand=0, side="left", anchor="nw")
        add_btn = ttk.Button(option_group_fr, text="Add")
        add_btn.grid(row=0, column=0)
        update_btn = ttk.Button(option_group_fr, text="Update")
        update_btn.grid(row=0, column=1)
        delete_btn = ttk.Button(option_group_fr, text="Delete")
        delete_btn.grid(row=0, column=2)

        search_group_fr = ttk.Frame(header_fr, borderwidth=1, border=1, relief=tk.RIDGE)
        search_group_fr.pack(fill=tk.X, expand=0, side="right", anchor="ne")
        search_entry = ttk.Entry(search_group_fr, width=70)
        search_entry.grid(row=0, column=3)
        search_btn = ttk.Button(search_group_fr, text="Tìm kiếm")
        search_btn.grid(row=0, column=4)

        self.__ui_left_view(root, main_fr)
        style = ttk.Style()
        style.theme_use('default')
        style.configure("BGR1.TFrame", background="#CC6600")

        self.right_fr = ttk.Frame(main_fr, borderwidth=1, border=1, relief=tk.RIDGE)
        self.right_fr.pack(fill=tk.Y, expand=0, side="right")

        # default right content
        self.product_page()

    def __ui_left_view(self, root, main_fr):
        style = ttk.Style()
        style.theme_use('default')
        left_fr = ttk.Frame(main_fr, borderwidth=1, border=1, relief=tk.RIDGE)
        left_fr.pack(fill=tk.Y, expand=0, side="left", anchor="nw")
        revenue_btn = ttk.Button(left_fr, text="Doanh thu", width=20,
                                 command=lambda: self.__switch_page(root, main_fr, page=""))
        revenue_btn.grid(row=0, column=0)
        salary_btn = ttk.Button(left_fr, text="Lương nhân viên", width=20,
                                command=lambda: self.__switch_page(root, main_fr, page="SALARY"))
        salary_btn.grid(row=1, column=0)

    def ui_right_content_view(self):
        style = ttk.Style()
        style.theme_use('default')
        table_fr = ttk.Frame(self.right_fr, style="BGR1.TFrame")
        table_fr.grid(row=1, column=0)

        self.t = ttk.Treeview(table_fr)
        self.t.pack(fill=tk.BOTH, expand=1, padx=20, pady=10)

        style.configure("Treeview.Heading", background="#000099",
                        foreground="white")
        self.t["columns"] = (
        "id", "user_create", "create_date", "customer_name", "customer_phone", "table_num", "total_money")
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

    def product_page(self):
        self.ui_right_content_view()



    def __switch_page(self, root, main_fr, page):
        for fr in self.right_fr.winfo_children():
            fr.destroy()
            root.update()
        if page == "SALARY":
            self.promotion_page(main_fr)
        else:
            self.product_page()
    def data_example(self):
        bills = (200, 300)
        return bills

    def promotion_page(self, main_fr):
        # add employee frame
        promotion_fr = ttk.Frame(self.right_fr)
        lb = ttk.Label(promotion_fr, text="Promotion Page")
        lb.pack()
        promotion_fr.pack()

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(True, True)
    root.state('zoomed')  # full screen
    root.title("Ware House View")
    root.config(background="blue")
    rp = WareHouseView(root)
    root.mainloop()
