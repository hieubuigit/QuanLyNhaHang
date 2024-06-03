import base64
import io
import math
from decimal import Decimal

import customtkinter as ctk
import tkinter as tk
from PIL import Image


class MenuFoodView:

    def __init__(self, parent, controller, reload_table_page, table_info):
        # Property
        self.__controller = controller
        self.reload_table_page = reload_table_page
        self._quantity_selected_var = tk.IntVar()
        self.__transience_var = tk.StringVar(value="0")
        self._money_to_pay_var = tk.StringVar(value="0")
        self.__tax_rate = 8
        self.__service__charge_rate = 10
        self.__table_info = table_info
        self.__discount_percent_var = tk.StringVar()
        self.__customer_phone_var = tk.StringVar()
        self.__customer_name_var = tk.StringVar()

        # Setup UI
        global toplevel, font_title1, half_width
        font_title1 = ctk.CTkFont("Roboto", 16)
        toplevel = ctk.CTkToplevel(parent)
        toplevel.resizable(True, False)
        toplevel.geometry("1350x800")
        toplevel.state('zoomed')
        toplevel.title("Thực đơn nhà hàng")
        half_width = 669
        print(half_width)
        self.validation = toplevel.register(self.validate_input)

        self.create_ui_bill(toplevel)
        self.create_ui_menu(toplevel)

        # Add các món ăn vào hóa đơn
        self.setup_data_bill()
        bill_id = self.__controller.bill_id
        bill_num.configure(text=f"Hóa đơn: {bill_id}")

        percents = self.__controller.get_discount_percents()
        discount_cbb.configure(values=percents)



    def validate_input(self, text):
        # Chỉ cho phép chữ số
        if text.isdigit():
            return True
        else:
            return False
    def create_ui_bill(self, parent):
        global order_fr, bill_num, orders_canvas, discount_cbb
        bill_fr = ctk.CTkFrame(parent)
        bill_fr.pack(side=tk.LEFT, fill=tk.Y, expand=0)
        # UI Thông tin khách hàng, thông tin bàn
        header_bill_fr = ctk.CTkFrame(bill_fr, fg_color="white", corner_radius=0)
        customer_info_fr = ctk.CTkFrame(header_bill_fr)
        customer_info_fr.pack(fill=tk.X, expand=0, side="left", padx=10)
        customer_name_lb = ctk.CTkLabel(customer_info_fr, text="Họ tên KH", font=font_title1)
        customer_name_lb.grid(row=0, column=0, sticky="w", padx=5)
        customer_name_entry = ctk.CTkEntry(customer_info_fr, placeholder_text="Nhập họ tên khách hàng",
                                           width=250, textvariable=self.__customer_name_var)
        customer_name_entry.grid(row=0, column=1)
        customer_phone = ctk.CTkLabel(customer_info_fr, text="Số điện thoại KH", font=font_title1)
        customer_phone.grid(row=1, column=0, padx=5, sticky="w")
        customer_phone_entry = ctk.CTkEntry(customer_info_fr, textvariable=self.__customer_phone_var,
                                            placeholder_text="Nhập số điện thoại khách hàng", width=250,
                                            validatecommand=(self.validation, '%S'), validate="key")
        customer_phone_entry.grid(row=1, column=1, pady=5)
        right_fr = ctk.CTkFrame(header_bill_fr)
        right_fr.pack()
        bill_num = ctk.CTkLabel(right_fr, text=f"Hóa đơn: {0}", anchor="nw", font=font_title1)
        bill_num.pack(fill=tk.X, expand=0)
        table_num_info = ctk.CTkLabel(right_fr,
                                      text=f"Bàn: {self.__table_info.tableNum}", anchor="nw",
                                      font=font_title1)
        table_num_info.pack(fill=tk.X, expand=0)
        seat_num_lb = ctk.CTkLabel(right_fr, text=f"Số người: {self.__table_info.seatNum}", anchor="nw",
                                   font=font_title1)
        seat_num_lb.pack(fill=tk.X, expand=0)
        header_bill_fr.pack(fill=tk.X, expand=0, pady=10)

        # UI danh sách các món ăn được chọn
        header_table = ctk.CTkFrame(bill_fr, fg_color="white")
        header_table.pack(fill=tk.X, expand=0)
        product_name = ctk.CTkButton(header_table, text="Tên món", corner_radius=0,
                                     fg_color="#33CCFF", text_color="black", border_width=1, state="readonly")
        product_name.grid(row=0, column=0)
        quantity_lb = ctk.CTkButton(header_table, text="Số lượng", corner_radius=0,
                                    border_width=1, width=160, state="readonly",
                                    fg_color="#33CCFF", text_color="black")
        quantity_lb.grid(row=0, column=1)

        unit_price_lb = ctk.CTkButton(header_table, text="Đơn giá", corner_radius=0, border_width=1, state="readonly",
                                      fg_color="#33CCFF", text_color="black")
        unit_price_lb.grid(row=0, column=2)
        into_money_lb = ctk.CTkButton(header_table, text="Thành tiền", corner_radius=0, border_width=1,
                                      state="readonly", fg_color="#33CCFF", text_color="black")
        into_money_lb.grid(row=0, column=3)
        del_fr = ctk.CTkFrame(header_table, width=60, height=35)
        del_fr.grid(row=0, column=4)
        bill_content_fr = ctk.CTkFrame(bill_fr, fg_color="white")
        bill_content_fr.pack(fill=tk.BOTH, expand=1)

        # Tạo thanh cuộn dọc
        order_vertical_sb = ctk.CTkScrollbar(bill_content_fr, orientation="vertical")
        order_vertical_sb.pack(side="right", fill="y")

        # Tạo một canvas để chứa
        orders_canvas = ctk.CTkCanvas(bill_content_fr,
                                    yscrollcommand=order_vertical_sb.set, background="white")

        orders_canvas.pack(fill=tk.BOTH, expand=True, side="left")
        orders_canvas.bind('<Configure>', lambda e: orders_canvas.configure(scrollregion=orders_canvas.bbox("all")))

        order_fr = ctk.CTkFrame(orders_canvas, fg_color="white", corner_radius=0)
        orders_canvas.create_window((0, 0), window=order_fr, anchor="nw")
        # Kết nối thanh cuộn với canvas
        order_vertical_sb.configure(command=orders_canvas.yview)

        # UI Tiền tạm tính, Thuế, phí dịch vụ, khuyễn mãi, Tổng tiền, chức năng thanh toán
        bottom_bill_fr = ctk.CTkFrame(bill_fr, height=100, fg_color="#33CCFF", corner_radius=8)
        bottom_bill_fr.pack(side=tk.BOTTOM, fill=tk.X, expand=0)
        info_money = ctk.CTkFrame(bottom_bill_fr, fg_color="transparent")
        info_money.pack(side=tk.LEFT, expand=0, padx=(30, 10), pady=20)
        total_money_lb = ctk.CTkLabel(info_money, text="Tạm tính (đ)", fg_color="transparent",
                                      font=font_title1)
        total_money_lb.grid(row=0, column=0)
        total_money_btn = ctk.CTkButton(info_money, fg_color="transparent",
                                        text_color="black", anchor="w", state="readonly",
                                        textvariable=self.__transience_var)
        total_money_btn.grid(row=0, column=1)
        vat_lb = ctk.CTkLabel(info_money, text="VAT", fg_color="transparent", font=font_title1)
        vat_lb.grid(row=1, column=0)
        vat_btn = ctk.CTkButton(info_money, text="8%", fg_color="transparent",
                                text_color="black", anchor="w", state="readonly")
        vat_btn.grid(row=1, column=1)
        service_charge_rate_lb = ctk.CTkLabel(info_money, text="Phí dịch vụ", fg_color="transparent",
                                              font=font_title1)
        service_charge_rate_lb.grid(row=2, column=0)
        service_charge_rate_value = ctk.CTkButton(info_money, text="10%", fg_color="transparent",
                                text_color="black", anchor="w", state="readonly")
        service_charge_rate_value.grid(row=2, column=1)

        discount_lb = ctk.CTkLabel(info_money, text="Khuyến mãi", fg_color="transparent", font=font_title1)
        discount_lb.grid(row=3, column=0, padx=(0, 5))
        discount_cbb = ctk.CTkComboBox(info_money, variable=self.__discount_percent_var)
        discount_cbb.grid(row=3, column=1)

        discount_btn = ctk.CTkButton(info_money, text="Áp dụng", fg_color="green", width=60, corner_radius=5,
                                     text_color="white", command=lambda: self.apply_onclick())
        discount_btn.grid(row=3, column=2, padx=(5, 0))

        money_to_pay_fr = ctk.CTkFrame(bottom_bill_fr, fg_color="transparent")
        money_to_pay_fr.pack(side="right", pady=20, padx=20)
        money_to_pay_lb = ctk.CTkLabel(money_to_pay_fr, text="Tổng tiền (đ)", fg_color="transparent",
                                       font=font_title1)
        money_to_pay_lb.pack()
        money_to_pay_btn = ctk.CTkButton(money_to_pay_fr, text="2000000", fg_color="transparent",
                                         text_color="black", state="readonly",
                                         textvariable=self._money_to_pay_var)
        money_to_pay_btn.pack()
        payment_btn = ctk.CTkButton(money_to_pay_fr, text="Thanh toán", height=40, corner_radius=5,
                                    fg_color="#007700", command=lambda: self.payment_onclick())
        payment_btn.pack(padx=10)

    def update_scroll_region(self):
        order_fr.update_idletasks()
        orders_canvas.config(scrollregion=orders_canvas.bbox("all"))
    def create_row_bill(self, parent, row_num, item_order):
        global quantity_selected_var, into_money_var
        quantity_selected_var = tk.StringVar()
        into_money_var = tk.StringVar()
        obi_food = self.__controller.get_product_by_id(item_order.product_id)
        row_fr = ctk.CTkFrame(parent)
        row_fr.pack(fill=tk.BOTH, expand=1)
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

        unit_price_value = ctk.CTkButton(row_fr, text=f"{obi_food.price:0,.0f}", corner_radius=0, fg_color="white",
                                         text_color="black", state="readonly")
        unit_price_value.grid(row=row_num, column=2)
        into_money_var.set(f"{item_order.cur_price:0,.0f}")
        into_money_value = ctk.CTkButton(row_fr, corner_radius=0, fg_color="transparent",
                                         text_color="black", state="readonly", textvariable=into_money_var)
        into_money_value.grid(row=row_num, column=3)
        img_delete = ctk.CTkImage(Image.open("../assets/delete.png"), size=(20, 20))
        delete_btn = ctk.CTkButton(row_fr, text="", image=img_delete, width=35, height=35, corner_radius=0,
                                   fg_color="transparent", hover_color="pink",
                                   command=lambda obj=item_order: self.delete_food_in_bill(obj))
        delete_btn.grid(row=row_num, column=4)
        line = ctk.CTkFrame(parent, fg_color="#33CCFF", height=1)
        line.pack(expand=0, fill=tk.X)

    def delete_food_in_bill(self, order_food):
        if self.__controller.delete_order_list_by_id(order_food.id):
            for child in order_fr.winfo_children():
                child.destroy()
            self.setup_data_bill()

    def setup_data_bill(self):
        order_list = self.__controller.get_order_list_by_id()
        if order_list:
            for index, item in enumerate(order_list):
                self.create_row_bill(order_fr, index, item)
            self.update_scroll_region()
            self.calculate_bill()

    def create_ui_menu(self, parent):
        global toplevel, menu_canvas, menu_fr

        menu_content = ctk.CTkFrame(parent, width=half_width)
        menu_content.pack(fill=tk.BOTH, expand=1, side=tk.RIGHT)
        # menu_content.pack_propagate(False)

        # Tạo thanh cuộn dọc
        vertical_sb = ctk.CTkScrollbar(menu_content, orientation="vertical")
        vertical_sb.pack(side="right", fill="y")

        # Tạo một canvas để chứa lưới
        menu_canvas = ctk.CTkCanvas(menu_content,
                                    yscrollcommand=vertical_sb.set, background="white")
        menu_canvas.pack(fill=tk.BOTH, expand=True, side="left")
        menu_canvas.bind('<Configure>', lambda e: menu_canvas.configure(scrollregion=menu_canvas.bbox("all")))

        # Kết nối thanh cuộn với canvas
        vertical_sb.configure(command=menu_canvas.yview)

        # Tạo một frame con để chứa món ăn
        menu_fr = ctk.CTkFrame(menu_canvas, fg_color="white", corner_radius=0)
        menu_canvas.create_window((0, 0), window=menu_fr, anchor="ne")
        
        # Thêm món ăn vào menu
        _foods = self.__controller.foods
        self._insert_food_to_menu(menu_fr, _foods)

    def _insert_food_to_menu(self, menu_fr, foods):
        if len(foods) <= 0:
            return
        num_columns = 3
        num_rows = math.ceil(len(foods) / num_columns)
        for i in range(num_rows):
            for j in range(num_columns):
                index = i * num_columns + j
                if index < len(foods):
                    menu_fr.grid_columnconfigure(j, weight=1)
                    sub_menu_fr = ctk.CTkFrame(menu_fr, border_width=0, fg_color="pink")
                    sub_menu_fr.grid(row=i, column=j, sticky="nsew", padx=3, pady=3)
                    sub_menu_fr.bind("<Button-1>", lambda e, f=foods[index]: self.food_selected(f))
                    img_default = ctk.CTkImage(Image.open("../assets/dish_default.png"), size=(80, 80))
                    food_image = ctk.CTkButton(sub_menu_fr, text="", corner_radius=0, width=80, height=80,
                                               fg_color="white", image=img_default, border_width=1,
                                               border_color="red", state="readonly")
                    food_image.grid(row=index, column=0, pady=4, padx=4)
                    food_image.bind("<Button-1>", lambda e, f=foods[index]: self.food_selected(f))
                    if foods[index].image:
                        image_decode = foods[index].image + b'=' * (-len(foods[index].image) % 4)
                        de = base64.b64decode(image_decode)
                        image = Image.open(io.BytesIO(de))
                        photo = ctk.CTkImage(image, size=(80, 80))
                        food_image.configure(image=photo)
                    right_fr = ctk.CTkFrame(sub_menu_fr, corner_radius=0, fg_color="transparent")
                    right_fr.grid(row=index, column=1, padx=(10, 20))
                    right_fr.bind("<Button-1>", lambda e, f=foods[index]: self.food_selected(f))
                    food_name_lb = ctk.CTkLabel(right_fr, text=f"{foods[index].name}", fg_color="transparent",
                                                wraplength=110, anchor="w", justify="left")
                    food_name_lb.pack(expand=0)
                    food_name_lb.bind("<Button-1>", lambda e, f=foods[index]: self.food_selected(f))

                    price_lb = ctk.CTkLabel(right_fr, text=f"{foods[index].price} đ", fg_color="transparent")
                    price_lb.pack(expand=0)
                    price_lb.bind("<Button-1>", lambda e, f=foods[index]: self.food_selected(f))

    def food_selected(self, food):
        self.__controller.create_order_list(food=food, quantity_selected=1)
        for child in order_fr.winfo_children():
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


    def apply_onclick(self):
        print("apply")
        discount_percent = Decimal(self.__discount_percent_var.get())
        self.calculate_bill(discount_percent)
    def update_quantity_and_reload(self, order_list, quantity, cur_price):
        if self.__controller.update_quantity(order_list_id=order_list.id, new_quantity=quantity, cur_price=cur_price):
            for widget in order_fr.winfo_children():
                widget.destroy()
            self.setup_data_bill()
    def payment_onclick(self):
        total = self._money_to_pay_var.get().replace(",", "")
        if self.__controller.update_bill(total_money=total, customer_name=self.__customer_name_var.get(),
                                         customer_phone=self.__customer_phone_var.get()):
            self.reload_table_page()
            toplevel.destroy()

    def __on_mouse_wheel(self, event):
        menu_canvas.yview("scroll", event.delta, "units")
        return "break"

    def calculate_bill(self, discount_percent=Decimal()):
        order_list = self.__controller.get_order_list_by_id()
        sub_total = sum(item.cur_price for item in order_list)
        sub_total_str = f"{sub_total:0,.0f}"
        self.__transience_var.set(sub_total_str)
        # Tính phí dịch vụ, mặc định phần trăm phí dị vụ 10%
        service_charge = sub_total * (self.__service__charge_rate / Decimal(100))

        # Tính thuế, mặc định phần trăm thuế 8%
        tax_value = sub_total * (self.__tax_rate / Decimal(100))

        # Tính giá trị chiết khấu
        discount_value = sub_total * (discount_percent / Decimal(100))

        # Tính tổng cộng
        total = sub_total + service_charge - discount_value + tax_value
        total_str = f"{total:0,.0f}"
        self._money_to_pay_var.set(total_str)

