import base64
import io
import tkinter as tk
from enum import Enum
from tkinter import ttk, messagebox
import customtkinter
from PIL import ImageTk, Image
from customtkinter import *
from tkinter import filedialog

from share.common_config import ProductType, UserType
from share.utils import Utils


class StatePage(Enum):
    Product = 0
    Discount = 1


class WareHouseView:
    def __init__(self, root, controller):
        # Property
        self.__controller = controller
        self.product_name_var = tk.StringVar()
        self.product_unit_var = tk.StringVar()
        self.product_price_var = tk.StringVar()
        self.product_quantity_var = tk.StringVar()
        self.product_capacity_var = tk.StringVar()
        self.product_alcohol_var = tk.StringVar()
        self.product_type_var = tk.StringVar()
        self.__search_var = tk.StringVar()
        self.__img_thumbnail_bytes = None
        self.dict_product_type = {ProductType.Food.value[0]: ProductType.Food.value[1],
                                  ProductType.Drink.value[0]: ProductType.Drink.value[1]}
        self.__product_id_selected = None
        self._user_type = Utils.user_profile["type"]
        # UI
        # style = ttk.Style()
        # style.theme_use("default")
        # Utils.set_appearance_mode(customtkinter)
        self.__ui_main_content(root=root)
        # default right content
        self.product_page()
        self.__current_page = StatePage.Product

    def __ui_main_content(self, root):

        main_fr = CTkFrame(root)
        main_fr.pack(fill="both", expand=True)

        header_fr = CTkFrame(main_fr, fg_color="transparent")
        header_fr.pack(fill=tk.X, expand=0, padx=10, pady=10)
        if self._user_type == UserType.ADMIN.value:
            option_group_fr = CTkFrame(header_fr, border_width=0)
            option_group_fr.pack(fill=tk.X, expand=0, side="left", anchor="nw")

            add_btn = CTkButton(option_group_fr,
                                text="Thêm mới",
                                corner_radius=18,
                                border_width=0,
                                height=36,
                                fg_color="DodgerBlue1",
                                hover_color="#63B8FF",
                                text_color="black",
                                font=CTkFont("TkDefaultFont", 16),
                                command=lambda: self.add_click())
            add_btn.grid(row=0, column=0)

            update_btn = CTkButton(option_group_fr,
                                   text="Chỉnh sửa",
                                   corner_radius=18,
                                   border_width=0,
                                   height=36,
                                   fg_color="LimeGreen",
                                   hover_color="#54FF9F",
                                   text_color="black",
                                   font=CTkFont("TkDefaultFont", 16),
                                   command=lambda: self.update_click())
            update_btn.grid(row=0, column=1, padx=5)

            delete_btn = CTkButton(option_group_fr,
                                   text="Xóa",
                                   corner_radius=18,
                                   border_width=0,
                                   height=36,
                                   fg_color="Firebrick1",
                                   hover_color="#FFC0CB",
                                   text_color="black",
                                   font=CTkFont("TkDefaultFont", 16),
                                   command=lambda: self.delete_click())
            delete_btn.grid(row=0, column=2)

        search_group_fr = CTkFrame(header_fr)
        search_group_fr.pack(fill=tk.X, expand=0, side="right", anchor="ne")
        search_entry = CTkEntry(search_group_fr,
                                placeholder_text="Nhập thông tin....",
                                placeholder_text_color="gray",
                                width=370,
                                height=35,
                                corner_radius=6,
                                fg_color="white",
                                textvariable=self.__search_var)
        search_entry.grid(row=0, column=3, padx=5)
        search_btn = CTkButton(search_group_fr,
                               text="Tìm kiếm",
                               corner_radius=6,
                               border_width=0,
                               height=36,
                               width=100,
                               fg_color="DodgerBlue1",
                               hover_color="#63B8FF",
                               text_color="black",
                               font=CTkFont("TkDefaultFont", 16),
                               command=lambda: self.search_onclick())
        search_btn.grid(row=0, column=4)

        self.__ui_left_view(root, main_fr)

        self.right_fr = CTkFrame(main_fr, border_width=1, border_color="gray")
        self.right_fr.pack(fill=tk.BOTH, expand=1, side="right", pady=10)

    def __ui_left_view(self, root, main_fr):
        left_fr = CTkFrame(main_fr, border_width=1, border_color="gray")
        left_fr.pack(fill=tk.Y, expand=0, side="left", anchor="nw", padx=10, pady=10, ipadx=2)
        gr_btn = CTkFrame(left_fr)
        gr_btn.pack(pady=3)
        img_product = CTkImage(Image.open("../assets/diet.png"), size=(25, 25))
        self.product_btn = CTkButton(gr_btn,
                                     text="Sản phẩm",
                                     width=150,
                                     height=30,
                                     corner_radius=1,
                                     image=img_product,
                                     compound=tk.LEFT,
                                     fg_color="white",
                                     text_color="#000080",
                                     hover_color="#63B8FF",
                                     command=lambda: self.__switch_page(root, page=StatePage.Product))
        self.product_btn.grid(row=0, column=0)
        img_discount = CTkImage(Image.open("../assets/discount.png"), size=(25, 25))
        self.product_line = CTkFrame(gr_btn, fg_color="#000080", height=30, width=2, corner_radius=0,
                                     border_width=0)
        self.product_line.grid(row=0, column=1)

        self.discount_btn = CTkButton(gr_btn,
                                      text="Khuyến mãi",
                                      width=150,
                                      height=30,
                                      corner_radius=1,
                                      fg_color="white",
                                      image=img_discount,
                                      compound=tk.LEFT,
                                      text_color="black",
                                      hover_color="#63B8FF",
                                      command=lambda: self.__switch_page(root, page=StatePage.Discount))
        self.discount_btn.grid(row=1, column=0)
        self.discount_line = CTkFrame(gr_btn, fg_color="white", height=30, width=2, corner_radius=0, border_width=0)
        self.discount_line.grid(row=1, column=1)

    def ui_right_content_view(self):
        style = ttk.Style()
        style.theme_use('default')

        self.tv = ttk.Treeview(self.right_fr)
        self.tv.pack(fill=tk.X, expand=0, padx=10, pady=10)

        style.configure("Treeview.Heading", background="DodgerBlue1", forceground="white", font=("TkDefaultFont", 18))
        self.tv["columns"] = ("id", "name", "unit", "price", "quantity", "capacity",
                              "alcohol", "type", "create_date")
        self.tv["show"] = "headings"
        self.tv.heading("#0", anchor="center")
        self.tv.column("id", anchor="center", width=80)
        self.tv.column("name", anchor="center")
        self.tv.column("unit", anchor="center", width=80)
        self.tv.column("price", anchor="center", width=100)
        self.tv.column("quantity", anchor="center", width=100)
        self.tv.column("capacity", anchor="center", width=100)
        self.tv.column("alcohol", anchor="center", width=140)
        self.tv.column("type", anchor="center", width=100)
        self.tv.column("create_date", anchor="center", width=100)

        self.tv.heading("#0", text="Product")
        self.tv.heading("id", text="ID")
        self.tv.heading("name", text="Tên")
        self.tv.heading("unit", text="Đơn vị")
        self.tv.heading("price", text="Giá")
        self.tv.heading("quantity", text="Số lượng")
        self.tv.heading("capacity", text="Dung tích")
        self.tv.heading("alcohol", text="Nồng độ cồn")
        self.tv.heading("type", text="Loại")
        self.tv.heading("create_date", text="Ngày tạo")
        self.tv.tag_configure("normal", background="white")
        self.tv.tag_configure("blue", background="lightblue")
        self.insert_row_treeview()
        if self._user_type == UserType.ADMIN.value:
            self.tv.bind("<<TreeviewSelect>>", lambda e: self.item_treeview_selected())
            # Setup UI Detail form
            self.ui_detail_form()

    def ui_detail_form(self):
        padding_x = 25
        padding_y = 5
        entry_width = 300
        entry_padding = 8
        line = CTkFrame(self.right_fr, height=1, fg_color="gray")
        line.pack(fill=tk.X, expand=0)

        option_fr = CTkFrame(self.right_fr, corner_radius=10, fg_color="white")
        option_fr.pack(expand=0, pady=10)

        heading2 = CTkFont("TkDefaultFont", 16, 'bold')

        detail_lb = CTkLabel(option_fr, text="Thông tin chi tiết", text_color="#000088",
                             font=heading2)
        detail_lb.pack(fill=tk.X, expand=0, padx=20, side="top", pady=5)

        self.sub_fr = CTkFrame(option_fr, fg_color="white")
        self.sub_fr.pack(fill=tk.X, expand=0, padx=padding_x, pady=padding_y, ipadx=10)

        product_name_lb = CTkLabel(self.sub_fr, text="Tên")
        product_name_lb.grid(row=0, column=0, sticky=(tk.N, tk.W), pady=entry_padding, padx=entry_padding)

        product_name_entry = CTkEntry(self.sub_fr, entry_width, textvariable=self.product_name_var)
        product_name_entry.grid(row=0, column=1, pady=entry_padding)

        unit_lb = CTkLabel(self.sub_fr, text="Đơn vị")
        unit_lb.grid(row=1, column=0, sticky=(tk.N, tk.W), padx=entry_padding, pady=entry_padding)

        unit_entry = CTkEntry(self.sub_fr, entry_width, textvariable=self.product_unit_var)
        unit_entry.grid(row=1, column=1)

        price_lb = CTkLabel(self.sub_fr, text="Giá")
        price_lb.grid(row=2, column=0, sticky=(tk.N, tk.W), pady=entry_padding, padx=entry_padding)

        price_entry = CTkEntry(self.sub_fr, entry_width, textvariable=self.product_price_var)
        price_entry.grid(row=2, column=1, sticky=(tk.N, tk.W), pady=entry_padding, padx=entry_padding)

        quantity_lb = CTkLabel(self.sub_fr, text="Số lượng")
        quantity_lb.grid(row=3, column=0, sticky=(tk.N, tk.W), pady=entry_padding, padx=entry_padding)

        quantity_entry = CTkEntry(self.sub_fr, entry_width, textvariable=self.product_quantity_var)
        quantity_entry.grid(row=3, column=1, sticky=(tk.N, tk.W), pady=entry_padding, padx=entry_padding)

        product_type_lb = CTkLabel(self.sub_fr, text="Loại")
        product_type_lb.grid(row=4, column=0, sticky=(tk.N, tk.W), pady=entry_padding, padx=entry_padding)

        product_type_cbb = CTkComboBox(self.sub_fr, entry_width, values=list(self.dict_product_type.values()),
                                       variable=self.product_type_var)
        product_type_cbb.grid(row=4, column=1, pady=entry_padding, padx=entry_padding)

        capacity_lb = CTkLabel(self.sub_fr, text="Dung tích")
        capacity_lb.grid(row=0, column=2, sticky=(tk.N, tk.W), padx=30, pady=entry_padding)

        capacity_entry = CTkEntry(self.sub_fr, entry_width, textvariable=self.product_capacity_var)
        capacity_entry.grid(row=0, column=3)

        alcohol_lb = CTkLabel(self.sub_fr, text="Nồng độ cồn")
        alcohol_lb.grid(row=1, column=2, sticky=(tk.N, tk.W), pady=entry_padding, padx=30)

        alcohol_entry = CTkEntry(self.sub_fr, entry_width, textvariable=self.product_alcohol_var)
        alcohol_entry.grid(row=1, column=3, pady=entry_padding)

        image_lb = CTkLabel(self.sub_fr, text="Hình ảnh")
        image_lb.grid(row=5, column=0, sticky=(tk.N, tk.W, tk.S), pady=entry_padding, padx=entry_padding)
        img_table = CTkImage(Image.open("../assets/add.png"), size=(50, 50))

        self.add_img_btn = CTkButton(self.sub_fr, text="", image=img_table, width=100, height=100, corner_radius=5,
                                     border_color="green", border_width=1, command=lambda: self.show_file_dialog(),
                                     anchor="c", fg_color="white", hover_color="white")
        self.add_img_btn.grid(row=5, column=1, pady=entry_padding)

    def show_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Chọn hình",
                                               filetypes=(("jpeg", "*.jpg"), ("png", "*.png")))
        if file_path:
            try:
                # Mở hình ảnh
                with Image.open(file_path) as img:
                    if img.mode == "RGBA":
                        img = img.convert("RGB")
                    # Tạo thumbnail
                    thumbnail = img.copy()
                    thumbnail.thumbnail((80, 80))
                    # Chuyển đổi thumbnail thành dạng bytes
                    with io.BytesIO() as output:
                        thumbnail.save(output, format="JPEG")  # Chọn định dạng hình ảnh tuỳ thích
                        self.__img_thumbnail_bytes = output.getvalue()
                        image = CTkImage(img, size=(80, 80))
                        self.add_img_btn.configure(image=image)
            except IOError as e:
                print("Error:", e)

    def product_page(self):
        self.ui_right_content_view()

    def __switch_page(self, root, page):
        self.__current_page = page
        for fr in self.right_fr.winfo_children():
            fr.destroy()
            root.update()
        if page == StatePage.Discount:
            self.__controller.nav_discount_page(self.right_fr)
            self.discount_line.configure(fg_color="#000080")
            self.discount_btn.configure(text_color="#000080")
            self.product_line.configure(fg_color="white")
            self.product_btn.configure(text_color="black")

        else:
            self.product_page()
            self.product_line.configure(fg_color="#000080")
            self.product_btn.configure(text_color="#000080")
            self.discount_line.configure(fg_color="white")
            self.discount_btn.configure(text_color="black")

    def item_treeview_selected(self):
        selected_items = self.tv.selection()
        for item in selected_items:
            cols = self.tv.item(item, "values")
            self.__product_id_selected = cols[0]
            self.product_name_var.set(cols[1])
            self.product_unit_var.set(cols[2])
            self.product_price_var.set(cols[3].replace(",",""))
            self.product_quantity_var.set(cols[4])
            self.product_capacity_var.set(cols[5])
            self.product_alcohol_var.set(cols[6])
            self.product_type_var.set(self.dict_product_type.get(int(cols[7])))
            product = next((item for item in self.__controller.products if item.id == int(cols[0])), None)
            if product:
                if product.image:
                    image_decode = product.image + b'=' * (-len(product.image) % 4)
                    de = base64.b64decode(image_decode)
                    image = Image.open(io.BytesIO(de))
                    photo = CTkImage(image, size=(80, 80))
                    self.add_img_btn.configure(image=photo)
                    return

            img_add = CTkImage(Image.open("../assets/add.png"), size=(50, 50))
            self.add_img_btn.configure(image=img_add)

    def search_onclick(self):
        if self.__current_page == StatePage.Product:
            self.__controller.search_product(self.__search_var.get())
            self.reload_treeview()
            self.clear_form_detail()
        else:
            self.__controller.search_discount(self.__search_var.get())
    def add_click(self):
        if self.__current_page == StatePage.Product:
            image_encode = None
            if self.__img_thumbnail_bytes:
                image_encode = base64.b64encode(self.__img_thumbnail_bytes)
            if not self.is_validate_form_detail():
                product_type = ProductType.Drink.value[0] if self.product_type_var.get() == ProductType.Drink.value[
                    1] else ProductType.Food.value[0]
                self.__controller.add_new_and_reload(id=self.__product_id_selected,
                                                     name=self.product_name_var.get(),
                                                     price=self.product_price_var.get(),
                                                     unit=self.product_unit_var.get(),
                                                     quantity=self.product_quantity_var.get(),
                                                     capacity=self.product_capacity_var.get(),
                                                     alcohol=self.product_alcohol_var.get(),
                                                     productType=product_type,
                                                     image=image_encode)
                self.reload_treeview()
                self.clear_form_detail()
        else:
            self.__controller.add_discount()

    def is_validate_form_detail(self):
        mess = None
        if not self.product_name_var.get() or not self.product_price_var.get() or not self.product_type_var.get():
            mess = "Vui lòng nhập Tên, Giá, Loại"
        if mess:
            messagebox.showinfo(message=mess)
        print(mess)
        return mess

    def update_click(self):
        if self.__current_page == StatePage.Product:
            selected_items = self.tv.selection()
            if not selected_items:
                messagebox.showwarning("Thông báo", "Vui lòng chọn dòng muốn chỉnh sửa.")
                return
            image_encode = None
            if self.__img_thumbnail_bytes:
                image_encode = base64.b64encode(self.__img_thumbnail_bytes)
            for item in selected_items:
                item_id = self.tv.item(item, "values")[0]
                product_type = ProductType.Drink.value[0] if self.product_type_var.get() == ProductType.Drink.value[
                    1] else ProductType.Food.value[0]

                self.__controller.update_and_reload(id=item_id,
                                                    name=self.product_name_var.get(),
                                                    price=self.product_price_var.get(),
                                                    unit=self.product_unit_var.get(),
                                                    quantity=self.product_quantity_var.get(),
                                                    capacity=self.product_capacity_var.get(),
                                                    alcohol=self.product_alcohol_var.get(),
                                                    product_type=product_type,
                                                    image=image_encode)
            self.reload_treeview()
            self.clear_form_detail()

        else:
            self.__controller.update_row_discount()

    def delete_click(self):
        if self.__current_page == StatePage.Product:
            selected_items = self.tv.selection()
            if not selected_items:
                messagebox.showwarning("Thông báo", "Vui lòng chọn dòng muốn xóa.")
                return
            if messagebox.askokcancel(title="Thông báo", message="Bạn có chắc chắn muốn xóa sản phẩm này không?"):
                for item in selected_items:
                    item_id = self.tv.item(item, "values")[0]
                    self.tv.delete(item)
                    self.__controller.delete_and_reload(id=item_id)
                self.reload_treeview()
                self.clear_form_detail()

        else:
            self.__controller.delete_row_discount()

    def reload_treeview(self):
        for item in self.tv.get_children():
            self.tv.delete(item)
        self.insert_row_treeview()

    def insert_row_treeview(self):
        products = self.__controller.products
        if products:
            for p in products:
                # ("id", "name", "unit", "price", "quantity", "capacity",
                #  "alcohol", "type", "create_date", "update_date")
                self.tv.insert("", "end", iid=p.id, text=p.id,
                               values=(p.id, p.name, p.unit, f"{p.price:0,.0f}", p.quantity,
                                       p.capacity, p.alcohol, p.productType, f"{p.createdDate:%Y-%m-%d}"))

    def clear_form_detail(self):
        self.product_name_var.set("")
        self.product_unit_var.set("")
        self.product_price_var.set("")
        self.product_quantity_var.set("")
        self.product_type_var.set("")
        self.product_alcohol_var.set("")
        self.product_capacity_var.set("")
        img_add = CTkImage(Image.open("../assets/add.png"), size=(50, 50))
        self.add_img_btn.configure(image=img_add)
        self.__img_thumbnail_bytes = None
        self.__product_id_selected = None
