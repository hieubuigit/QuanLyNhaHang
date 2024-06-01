import base64
import io
import customtkinter as ctk
import tkinter as tk
from PIL import Image


class MenuFood:
    def __init__(self, parent, controller):
        # Property
        self.__controller = controller
        self._quantity_selected_var = tk.IntVar()
        self._total_money_var = tk.StringVar(value="0")
        self._money_to_pay_var = tk.StringVar(value="0")

        # Setup UI
        toplevel = ctk.CTkToplevel(parent)
        toplevel.resizable(True, False)
        toplevel.geometry("1000x700")
        toplevel.title("Thực đơn nhà hàng")
        toplevel.protocol("WM_DELETE_WINDOW", lambda: self.on_toplevel_closing(toplevel))
        self.create_ui_bill(toplevel)
        self.create_ui_menu(toplevel)

    def on_toplevel_closing(self, toplevel):
        self.__controller.update_quantity()
        # toplevel.destroy()

    def create_ui_bill(self, parent):
        bill_fr = ctk.CTkFrame(parent)
        bill_fr.pack(side=tk.LEFT, fill=tk.Y, expand=0)
        # UI Thông tin khách hang
        header_bill_fr = ctk.CTkFrame(bill_fr, fg_color="white", corner_radius=0)
        table_num_info = ctk.CTkLabel(header_bill_fr, text=f"Số bàn: ABC")
        table_num_info.pack()
        header_bill_fr.pack(fill=tk.X, expand=0)
        # danh sách các món ăn được đặt
        header_table = ctk.CTkFrame(bill_fr)
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

        for i in range(1, 10):
            self.create_row_bill(bill_content_fr, i)

        # Tổng tiền, chức năng thanh toán
        bottom_bill_fr = ctk.CTkFrame(bill_fr, height=100, fg_color="#33CCFF", corner_radius=8)
        bottom_bill_fr.pack(side=tk.BOTTOM, fill=tk.X, expand=0)
        info_money = ctk.CTkFrame(bottom_bill_fr, fg_color="transparent")
        info_money.pack(side=tk.LEFT, expand=0, padx=20, pady=10)
        total_money_lb = ctk.CTkLabel(info_money, text="Tổng tiền", fg_color="transparent")
        total_money_lb.grid(row=0, column=0)
        total_money_btn = ctk.CTkButton(info_money, text="20000000đ", fg_color="transparent",
                                        text_color="black", anchor="w", state="readonly",
                                        textvariable=self._total_money_var)
        total_money_btn.grid(row=0, column=1)
        vat_lb = ctk.CTkLabel(info_money, text="VAT", fg_color="transparent")
        vat_lb.grid(row=1, column=0)
        vat_btn = ctk.CTkButton(info_money, text="20%", fg_color="transparent",
                                text_color="black", anchor="w", state="readonly")
        vat_btn.grid(row=1, column=1)
        money_to_pay_lb = ctk.CTkLabel(info_money, text="Thành tiền", fg_color="transparent")
        money_to_pay_lb.grid(row=2, column=0)
        money_to_pay_btn = ctk.CTkButton(info_money, text="2000000", fg_color="transparent",
                                         text_color="black", anchor="w", state="readonly",
                                         textvariable=self._money_to_pay_var)
        money_to_pay_btn.grid(row=2, column=1)
        # Nếu mới tạo bill thì text "Đặt món". Nếu có bill "Thanh toán"
        payment_btn = ctk.CTkButton(bottom_bill_fr, text="Đặt món", height=40, corner_radius=20, fg_color="#007700")
        payment_btn.pack(pady=30)

    def create_row_bill(self, parent, row_num):
        row_fr = ctk.CTkFrame(parent)
        row_fr.pack(fill=tk.X, expand=0)
        product_name_value = ctk.CTkButton(row_fr, text="Tên hàng hóa", corner_radius=0,
                                           fg_color="transparent", text_color="black", state="readonly")
        product_name_value.grid(row=row_num, column=0)
        # Group số lượng
        quantity_gr_fr = ctk.CTkFrame(row_fr, fg_color="transparent", width=160)
        quantity_gr_fr.grid(row=row_num, column=1, padx=5)
        minus_btn = ctk.CTkButton(quantity_gr_fr, text="-", width=50, fg_color="#CCCCCC",
                                  text_color="#000077", hover_color="#63B8FF",
                                  command=lambda: self.minus_onlick())
        minus_btn.grid(row=0, column=0)
        quantity_btn = ctk.CTkButton(quantity_gr_fr, corner_radius=0, text="0", fg_color="white",
                                     state="readonly", text_color="black", width=50,
                                     textvariable=self._quantity_selected_var)
        quantity_btn.grid(row=0, column=1)
        plus_btn = ctk.CTkButton(quantity_gr_fr, text="+", width=50, fg_color="#CCCCCC",
                                 text_color="#000077", hover_color="#63B8FF",
                                 command=lambda: self.plus_onclick())
        plus_btn.grid(row=0, column=2)

        unit_price_value = ctk.CTkButton(row_fr, text="Đơn giá", corner_radius=0, fg_color="transparent",
                                         text_color="black", state="readonly")
        unit_price_value.grid(row=row_num, column=2)
        into_money_value = ctk.CTkButton(row_fr, text="Thành tiền", corner_radius=0, fg_color="transparent",
                                         text_color="black", state="readonly")
        into_money_value.grid(row=row_num, column=3)
        delete_btn = ctk.CTkButton(row_fr, text="DEL", width=35, height=35, corner_radius=0,
                                   fg_color="transparent", text_color="red")
        delete_btn.grid(row=row_num, column=4)
        line = ctk.CTkFrame(parent, fg_color="red", height=1)
        line.pack(expand=0, fill=tk.X)


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
        self._insert_food_to_menu(menu_fr)



    def _insert_food_to_menu(self, menu_fr):
        global foods
        foods = self.__controller.foods
        if len(foods) <= 0:
            return
        for index, item in enumerate(foods):
            sub_menu_fr = ctk.CTkFrame(menu_fr, border_width=1, border_color="gray", fg_color="white")
            sub_menu_fr.pack(fill=tk.X, expand=0, padx=20, pady=3)
            food_image = ctk.CTkButton(sub_menu_fr, text="Image Food", width=100, height=100, corner_radius=0,
                                       border_width=1)
            food_image.grid(row=index, column=0, pady=4, padx=4)
            if item.image:
                image_decode = item.image + b'=' * (-len(item.image) % 4)
                de = base64.b64decode(image_decode)
                image = Image.open(io.BytesIO(de))
                photo = ctk.CTkImage(image, size=(100, 100))
                food_image.configure(image=photo, text="")
            right_fr = ctk.CTkFrame(sub_menu_fr, corner_radius=0, fg_color="white")
            right_fr.grid(row=index, column=1, padx=(40, 20))
            food_name_lb = ctk.CTkLabel(right_fr, text=f"{item.name}")
            food_name_lb.pack(expand=0)
            price_lb = ctk.CTkLabel(right_fr, text=f"{item.price} đ")
            price_lb.pack(expand=0)


    def minus_onlick(self):
        if self._quantity_selected_var.get() < 1:
            return
        for widget in menu_fr.winfo_children():
            widget.destroy()
        self._insert_food_to_menu()
        #Cập nhật số lượng, giá tiền, thành tiền
        # self._quantity_selected_var.set(int(self._quantity_selected_var.get()) - 1)

    def plus_onclick(self):
        print("plus_onlick")
        foods_selected = []
        # for i in foods:
        #     if i.id == obj_food.id:
        #         quantity = self._quantity_selected_var.get() + 1
        #         foods_selected.append(FoodModel(i.id, quantity))
        #
        # print("foods view", foods_selected)
        #
        # self.__controller.foods = foods
        # print("foods ctl", self.__controller.foods)
        # for widget in menu_fr.winfo_children():
        #     widget.destroy()
        # self._insert_food_to_menu()
        # #Cập nhật db, draw ui menu
        # self._insert_food_to_menu()
        # Cập nhật số lượng, giá tiền, thành tiền
        # self._quantity_selected_var.set(int(self._quantity_selected_var.get()) + 1)

    def order_or_payment_onclick(self):
        pass

    def __on_mouse_wheel(self, event):
        menu_canvas.yview("scroll", event.delta, "units")
        return "break"

class FoodModel:
    def __init__(self, id, quantity):
        self.__id = id
        self.__quantity = quantity