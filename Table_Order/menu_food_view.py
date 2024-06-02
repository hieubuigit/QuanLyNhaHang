import base64
import io
import math
from decimal import Decimal

import customtkinter as ctk
import tkinter as tk
from PIL import Image


class MenuFoodView:
    def __init__(self, parent, controller, reload_table_page):
        # Property
        self.__controller = controller
        self.reload_table_page = reload_table_page
        self._quantity_selected_var = tk.IntVar()
        self.__transience_var = tk.StringVar(value="0")
        self._money_to_pay_var = tk.StringVar(value="0")
        self.__tax_rate = 8
        self.__service__charge_rate = 10


        # Setup UI
        global toplevel
        toplevel = ctk.CTkToplevel(parent)
        toplevel.resizable(True, False)
        toplevel.geometry("1337x800")
        toplevel.title("Thực đơn nhà hàng")
        self.create_ui_bill(toplevel)
        self.create_ui_menu(toplevel)

        self.setup_data_bill()

    def create_ui_bill(self, parent):
        global bill_content_fr
        bill_fr = ctk.CTkFrame(parent)
        bill_fr.pack(side=tk.LEFT, fill=tk.Y, expand=0)
        # UI Thông tin khách hang
        header_bill_fr = ctk.CTkFrame(bill_fr, fg_color="white", corner_radius=0)
        table_num_info = ctk.CTkLabel(header_bill_fr, text=f"Số bàn: ABC")
        table_num_info.pack()
        header_bill_fr.pack(fill=tk.X, expand=0)
        # danh sách các món ăn được đặt
        header_table = ctk.CTkFrame(bill_fr, fg_color="white")
        header_table.pack(fill=tk.X, expand=0)
        product_name = ctk.CTkButton(header_table, text="Tên hàng hóa", corner_radius=0, border_width=1)
        product_name.grid(row=0, column=0)
        quantity_lb = ctk.CTkButton(header_table, text="Số lượng", corner_radius=0, border_width=1, width=160)
        quantity_lb.grid(row=0, column=1)

        unit_price_lb = ctk.CTkButton(header_table, text="Đơn giá", corner_radius=0, border_width=1)
        unit_price_lb.grid(row=0, column=2)
        into_money_lb = ctk.CTkButton(header_table, text="Thành tiền", corner_radius=0, border_width=1)
        into_money_lb.grid(row=0, column=3)

        bill_content_fr = ctk.CTkFrame(bill_fr, fg_color="transparent")
        bill_content_fr.pack(fill=tk.X, expand=0)

        # Tổng tiền, chức năng thanh toán
        bottom_bill_fr = ctk.CTkFrame(bill_fr, height=100, fg_color="#33CCFF", corner_radius=8)
        bottom_bill_fr.pack(side=tk.BOTTOM, fill=tk.X, expand=0)
        info_money = ctk.CTkFrame(bottom_bill_fr, fg_color="transparent")
        info_money.pack(side=tk.LEFT, expand=0, padx=(30, 10), pady=20)
        total_money_lb = ctk.CTkLabel(info_money, text="Tạm tính (đ)", fg_color="transparent")
        total_money_lb.grid(row=0, column=0)
        total_money_btn = ctk.CTkButton(info_money, fg_color="transparent",
                                        text_color="black", anchor="w", state="readonly",
                                        textvariable=self.__transience_var)
        total_money_btn.grid(row=0, column=1)
        vat_lb = ctk.CTkLabel(info_money, text="VAT", fg_color="transparent")
        vat_lb.grid(row=1, column=0)
        vat_btn = ctk.CTkButton(info_money, text="8%", fg_color="transparent",
                                text_color="black", anchor="w", state="readonly")
        vat_btn.grid(row=1, column=1)
        service_charge_rate_lb = ctk.CTkLabel(info_money, text="Phí dịch vụ", fg_color="transparent")
        service_charge_rate_lb.grid(row=2, column=0)
        service_charge_rate_value = ctk.CTkButton(info_money, text="10%", fg_color="transparent",
                                text_color="black", anchor="w", state="readonly")
        service_charge_rate_value.grid(row=2, column=1)

        discount_lb = ctk.CTkLabel(info_money, text="Khuyến mãi", fg_color="transparent")
        discount_lb.grid(row=3, column=0, padx=(0, 5))
        discount_percent = []
        discount_cbb = ctk.CTkComboBox(info_money, values=discount_percent,
                                       state="readonly")
        discount_cbb.grid(row=3, column=1)
        percents = self.__controller.get_discount_percents()
        print("percents", len(percents))
        discount_btn = ctk.CTkButton(info_money, text="Áp dụng", fg_color="green", width=60,
                                     text_color="black",  state="readonly")
        discount_btn.grid(row=3, column=2, padx=(5, 0))

        money_to_pay_fr = ctk.CTkFrame(bottom_bill_fr, fg_color="transparent")
        money_to_pay_fr.pack(side="right", pady=20, padx=20)
        money_to_pay_lb = ctk.CTkLabel(money_to_pay_fr, text="Tổng tiền (đ)", fg_color="transparent")
        money_to_pay_lb.pack()
        money_to_pay_btn = ctk.CTkButton(money_to_pay_fr, text="2000000", fg_color="transparent",
                                         text_color="black", state="readonly",
                                         textvariable=self._money_to_pay_var)
        money_to_pay_btn.pack()
        payment_btn = ctk.CTkButton(money_to_pay_fr, text="Thanh toán", height=40, corner_radius=5,
                                    fg_color="#007700", command=lambda: self.payment_onclick())
        payment_btn.pack(padx=10)

    def create_row_bill(self, parent, row_num, item_order):
        global quantity_selected_var, into_money_var
        quantity_selected_var = tk.StringVar()
        into_money_var = tk.StringVar()
        obi_food = self.__controller.get_product_by_id(item_order.product_id)
        row_fr = ctk.CTkFrame(parent)
        row_fr.pack(fill=tk.X, expand=0)
        product_name_value = ctk.CTkButton(row_fr, text=obi_food.name, corner_radius=0,
                                           fg_color="transparent", text_color="black", state="readonly")
        product_name_value.grid(row=row_num, column=0)
        # Group số lượng
        quantity_gr_fr = ctk.CTkFrame(row_fr)
        quantity_gr_fr.grid(row=row_num, column=1, padx=10)
        minus_btn = ctk.CTkButton(quantity_gr_fr, text="-", width=40, fg_color="#CCCCCC",
                                  text_color="#000077", hover_color="#63B8FF",
                                  command=lambda obj=item_order, f=obi_food: self.minus_onlick(order_list=obj, food=f))
        minus_btn.grid(row=0, column=0)
        quantity_selected_var.set(item_order.quantity)
        quantity_btn = ctk.CTkButton(quantity_gr_fr, corner_radius=0, fg_color="white",
                                     state="readonly", text_color="black", width=60,
                                     textvariable=quantity_selected_var)
        quantity_btn.grid(row=0, column=1)
        plus_btn = ctk.CTkButton(quantity_gr_fr, text="+", width=40, fg_color="#CCCCCC",
                                 text_color="#000077", hover_color="#63B8FF",
                                 command=lambda obj=item_order, f=obi_food: self.plus_onclick(order_list=obj, food=f))
        plus_btn.grid(row=0, column=2)

        unit_price_value = ctk.CTkButton(row_fr, text=obi_food.price, corner_radius=0, fg_color="pink",
                                         text_color="black", state="readonly")
        unit_price_value.grid(row=row_num, column=2)
        into_money_var.set(item_order.cur_price)
        into_money_value = ctk.CTkButton(row_fr, corner_radius=0, fg_color="transparent",
                                         text_color="black", state="readonly", textvariable=into_money_var)
        into_money_value.grid(row=row_num, column=3)
        img_delete = ctk.CTkImage(Image.open("../assets/delete.png"), size=(20, 20))
        delete_btn = ctk.CTkButton(row_fr, text="", image=img_delete, width=35, height=35, corner_radius=0,
                                   fg_color="transparent", hover_color="pink",
                                   command=lambda obj=item_order: self.delete_food_in_bill(obj))
        delete_btn.grid(row=row_num, column=4)
        line = ctk.CTkFrame(parent, fg_color="red", height=1)
        line.pack(expand=0, fill=tk.X)

    def delete_food_in_bill(self, order_food):
        if self.__controller.delete_order_list_by_id(order_food.id):
            for child in bill_content_fr.winfo_children():
                child.destroy()
            self.setup_data_bill()

    def setup_data_bill(self):
        order_list = self.__controller.get_order_list_by_id()
        if order_list:
            for index, item in enumerate(order_list):
                self.create_row_bill(bill_content_fr, index, item)
            self.calculate_bill()

    def create_ui_menu(self, parent):
        global toplevel, menu_canvas, menu_fr

        menu_content = ctk.CTkFrame(parent)
        menu_content.pack(fill=tk.BOTH, expand=1)
        # Tạo thanh cuộn dọc
        vertical_sb = ctk.CTkScrollbar(menu_content, orientation="vertical")
        vertical_sb.pack(side="right", fill="y")

        # Tạo một canvas để chứa lưới
        menu_canvas = ctk.CTkCanvas(menu_content,
                                    yscrollcommand=vertical_sb.set)
        menu_canvas.pack(fill=tk.BOTH, expand=True, side="left")
        menu_canvas.bind('<Configure>', lambda e: menu_canvas.configure(scrollregion=menu_canvas.bbox("all")))

        # Kết nối thanh cuộn với canvas
        vertical_sb.configure(command=menu_canvas.yview)

        # Tạo một frame con để chứa bàn
        menu_fr = ctk.CTkFrame(menu_canvas, fg_color="white", corner_radius=0)
        menu_canvas.create_window((0, 0), window=menu_fr, anchor="ne")
        menu_canvas.bind_all("<MouseWheel>", lambda e: self.__on_mouse_wheel(e))
        # Thêm món ăn vào menu
        _foods = self.__controller.foods
        self._insert_food_to_menu(menu_fr, _foods)

    def _insert_food_to_menu(self, menu_fr, foods):
        if len(foods) <= 0:
            return
        num_columns = 3
        image_size = 180
        num_rows = math.ceil(len(foods) / num_columns)
        for i in range(num_rows):
            for j in range(num_columns):
                index = i * num_columns + j
                if index < len(foods):
                    menu_fr.grid_columnconfigure(j, weight=1)
                    sub_menu_fr = ctk.CTkFrame(menu_fr, border_width=0, fg_color="pink")
                    sub_menu_fr.grid(row=i, column=j, sticky="nsew", padx=3, pady=3)
                    sub_menu_fr.bind("<Button-1>", lambda e, f=foods[index]: self.food_selected(e, f))
                    img_default = ctk.CTkImage(Image.open("../assets/dish_default.png"), size=(80, 80))
                    food_image = ctk.CTkButton(sub_menu_fr, text="", corner_radius=0, width=80, height=80,
                                               fg_color="white", image=img_default, border_width=1,
                                               border_color="red", state="readonly")
                    food_image.grid(row=index, column=0, pady=4, padx=4)
                    if foods[index].image:
                        image_decode = foods[index].image + b'=' * (-len(foods[index].image) % 4)
                        de = base64.b64decode(image_decode)
                        image = Image.open(io.BytesIO(de))
                        photo = ctk.CTkImage(image, size=(80, 80))
                        food_image.configure(image=photo)
                    right_fr = ctk.CTkFrame(sub_menu_fr, corner_radius=0, fg_color="transparent")
                    right_fr.grid(row=index, column=1, padx=(10, 20))
                    food_name_lb = ctk.CTkLabel(right_fr, text=f"{foods[index].name}", fg_color="transparent",
                                                wraplength=110, anchor="w", justify="left")
                    food_name_lb.pack(expand=0)
                    price_lb = ctk.CTkLabel(right_fr, text=f"{foods[index].price} đ", fg_color="transparent")
                    price_lb.pack(expand=0)
    def food_selected(self, event, food):
        self.__controller.create_order_list(food=food, quantity_selected=1)
        for child in bill_content_fr.winfo_children():
            child.destroy()
        self.setup_data_bill()

    def minus_onlick(self, order_list, food):
        if order_list.quantity <= 1:
            return
        quantity = order_list.quantity - 1
        cur_price = food.price * quantity
        self.update_quantity_and_reload(order_list=order_list, quantity=quantity, cur_price=cur_price)

    def plus_onclick(self, order_list, food):
        quantity = order_list.quantity + 1
        cur_price = food.price * quantity
        self.update_quantity_and_reload(order_list=order_list, quantity=quantity, cur_price=cur_price)

    def update_quantity_and_reload(self, order_list, quantity, cur_price):
        if self.__controller.update_quantity(order_list_id=order_list.id, new_quantity=quantity, cur_price=cur_price):
            for widget in bill_content_fr.winfo_children():
                widget.destroy()
            self.setup_data_bill()
    def payment_onclick(self):
        total = self._money_to_pay_var.get()
        if self.__controller.update_bill(total_money=total):
            self.reload_table_page()
            toplevel.destroy()

    def __on_mouse_wheel(self, event):
        menu_canvas.yview("scroll", event.delta, "units")
        return "break"

    def calculate_bill(self, discount=0):
        order_list = self.__controller.get_order_list_by_id()
        sub_total = sum(item.cur_price for item in order_list)
        sub_total_str = f"{sub_total:0,.0f}"
        self.__transience_var.set(sub_total_str)
        discount = 0
        # Tính phí dịch vụ, mặc định phần trăm phí dị vụ 10%
        service_charge = sub_total * (self.__service__charge_rate / Decimal(100))

        # Tính thuế, mặc định phần trăm thuế 8%
        tax = (sub_total - discount) * (self.__tax_rate / Decimal(100))

        # Tính tổng cộng
        total = sub_total + service_charge - discount + tax
        total_str = f"{total:0,.0f}"
        self._money_to_pay_var.set(total_str)

