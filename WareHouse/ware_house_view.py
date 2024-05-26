import base64
import io
import tkinter as tk
from enum import Enum
from tkinter import ttk, messagebox
import customtkinter
from PIL import ImageTk, Image, ImageFile
from customtkinter import *
from tkinter import filedialog

from WareHouse.discount_view import DiscountView


class StatePage(Enum):
    Product = 0
    Discount = 1

class WareHouseView:
    def __init__(self, root, controller):
        self.__controller = controller
        self.__ui_main_content(root=root)
        self.product_name_var = tk.StringVar()
        self.product_unit_var = tk.StringVar()
        self.product_price_var = tk.StringVar()
        self.product_quantity_var = tk.StringVar()
        self.product_capacity_var = tk.StringVar()
        self.product_alcohol_var = tk.StringVar()
        self.product_type_var = tk.StringVar()
        # default right content
        self.product_page()
        self.__current_page = StatePage.Product

    def __ui_main_content(self, root):

        customtkinter.set_appearance_mode("light")

        main_fr = CTkFrame(root)
        main_fr.pack(fill="both", expand=True)

        header_fr = CTkFrame(main_fr, fg_color="transparent")
        header_fr.pack(fill=tk.X, expand=0, padx=10, pady=10)

        option_group_fr = CTkFrame(header_fr, border_width=0)
        option_group_fr.pack(fill=tk.X, expand=0, side="left", anchor="nw")

        add_btn = CTkButton(option_group_fr, text="Thêm mới", corner_radius=4, border_width=0,
                            command=lambda: self.add_click())
        add_btn.grid(row=0, column=0)

        update_btn = CTkButton(option_group_fr, text="Chỉnh sửa", corner_radius=4, border_width=0,
                               command=lambda: self.update_click())
        update_btn.grid(row=0, column=1, padx=5)

        delete_btn = CTkButton(option_group_fr, text="Xóa", corner_radius=4, border_width=0,
                               command=lambda: self.delete_click())
        delete_btn.grid(row=0, column=2)

        search_group_fr = CTkFrame(header_fr)
        search_group_fr.pack(fill=tk.X, expand=0, side="right", anchor="ne")
        search_entry = CTkEntry(search_group_fr, placeholder_text="Nhập thông tin....", placeholder_text_color="gray",
                                width=370, corner_radius=0, fg_color="white")
        search_entry.grid(row=0, column=3, padx=5)
        search_btn = CTkButton(search_group_fr, text="Tìm kiếm", width=80, corner_radius=4, border_width=0)
        search_btn.grid(row=0, column=4)

        self.__ui_left_view(root, main_fr)

        self.right_fr = CTkFrame(main_fr, border_width=1, border_color="gray")
        self.right_fr.pack(fill=tk.BOTH, expand=1, side="right")

    def __ui_left_view(self, root, main_fr):
        left_fr = CTkFrame(main_fr, border_width=1, border_color="gray")
        left_fr.pack(fill=tk.Y, expand=0, side="left", anchor="nw", padx=10, pady=10)
        revenue_btn = CTkButton(left_fr, text="Sản phẩm", width=150, corner_radius=0,
                                command=lambda: self.__switch_page(root, page=StatePage.Product))
        revenue_btn.grid(row=0, column=0)
        salary_btn = CTkButton(left_fr, text="Khuyến mãi", width=150, corner_radius=0,
                               command=lambda: self.__switch_page(root, page=StatePage.Discount))
        salary_btn.grid(row=1, column=0, pady=2)

    def ui_right_content_view(self):
        style = ttk.Style()
        style.theme_use('default')
        table_fr = CTkFrame(self.right_fr, border_width=1, corner_radius=0)
        table_fr.grid(row=1, column=0, sticky=(tk.N, tk.E))
        self.right_fr.columnconfigure(0, weight=1)

        self.tv = ttk.Treeview(table_fr)
        self.tv.pack(fill=tk.BOTH, expand=1, padx=10, pady=10, side="right")

        style.configure("Treeview.Heading", background="#007BFF", forceground="white", font=("TkDefaultFont", 18))
        self.tv["columns"] = ("id", "name", "unit", "price", "quantity", "capacity",
                              "alcohol", "type", "create_date", "update_date")
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
        self.tv.column("update_date", anchor="center", width=140)

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
        self.tv.heading("update_date", text="Ngày Cập nhật")
        self.tv.tag_configure("normal", background="white")
        self.tv.tag_configure("blue", background="lightblue")
        self.insert_row_treeview()
        self.tv.bind("<<TreeviewSelect>>", lambda e: self.item_treeview_selected())

        line = CTkFrame(self.right_fr, height=1, fg_color="gray")
        line.grid(row=2, column=0, sticky=(tk.N, tk.E, tk.W, tk.S), pady=3)

        option_fr = CTkFrame(self.right_fr, corner_radius=0)
        option_fr.grid(row=3, column=0, sticky=(tk.N, tk.E, tk.S), padx=20)
        option_fr.columnconfigure(0, weight=1)
        option_fr.rowconfigure(0, weight=1)

        entry_width = 220
        entry_padding = 8
        heading2 = CTkFont("TkDefaultFont", 18, 'bold')
        title_option = CTkLabel(option_fr, text="Thông tin chi tiết", font=heading2)
        title_option.grid(row=0, column=0, sticky=(tk.N, tk.S), padx=entry_padding)

        product_name_lb = CTkLabel(option_fr, text="Tên")
        product_name_lb.grid(row=1, column=0, sticky=(tk.N, tk.W), pady=entry_padding, padx=entry_padding)

        product_name_entry = CTkEntry(option_fr, entry_width, textvariable=self.product_name_var)
        product_name_entry.grid(row=1, column=1, pady=entry_padding)

        unit_lb = CTkLabel(option_fr, text="Đơn vị")
        unit_lb.grid(row=2, column=0, sticky=(tk.N, tk.W), padx=entry_padding, pady=entry_padding)

        unit_entry = CTkEntry(option_fr, entry_width, textvariable=self.product_unit_var)
        unit_entry.grid(row=2, column=1)

        price_lb = CTkLabel(option_fr, text="Giá")
        price_lb.grid(row=3, column=0, sticky=(tk.N, tk.W), pady=entry_padding, padx=entry_padding)

        price_entry = CTkEntry(option_fr, entry_width, textvariable=self.product_price_var)
        price_entry.grid(row=3, column=1, sticky=(tk.N, tk.W), pady=entry_padding, padx=entry_padding)

        quantity_lb = CTkLabel(option_fr, text="Số lượng")
        quantity_lb.grid(row=4, column=0, sticky=(tk.N, tk.W), pady=entry_padding, padx=entry_padding)

        quantity_entry = CTkEntry(option_fr, entry_width, textvariable=self.product_quantity_var)
        quantity_entry.grid(row=4, column=1, sticky=(tk.N, tk.W), pady=entry_padding, padx=entry_padding)

        product_type_lb = CTkLabel(option_fr, text="Loại")
        product_type_lb.grid(row=5, column=0, sticky=(tk.N, tk.W), pady=entry_padding, padx=entry_padding)

        product_type_cbb = CTkComboBox(option_fr, entry_width, values=["Food", "Drink"], variable=self.product_type_var)
        product_type_cbb.grid(row=5, column=1, pady=entry_padding, padx=entry_padding)

        capacity_lb = CTkLabel(option_fr, text="Dung tích")
        capacity_lb.grid(row=1, column=2, sticky=(tk.N, tk.W), padx=30, pady=entry_padding)

        capacity_entry = CTkEntry(option_fr, entry_width, textvariable=self.product_capacity_var)
        capacity_entry.grid(row=1, column=3, padx=entry_padding)

        alcohol_lb = CTkLabel(option_fr, text="Nồng độ cồn")
        alcohol_lb.grid(row=2, column=2, sticky=(tk.N, tk.W), pady=entry_padding, padx=30)

        alcohol_entry = CTkEntry(option_fr, entry_width, textvariable=self.product_alcohol_var)
        alcohol_entry.grid(row=2, column=3, pady=entry_padding, padx=entry_padding)

        image_lb = CTkLabel(option_fr, text="Hình ảnh")
        image_lb.grid(row=6, column=0, sticky=(tk.N, tk.W, tk.S), pady=entry_padding, padx=entry_padding)
        img_table = ImageTk.PhotoImage(Image.open("../assets/ic_table_visible.png").resize((100, 100)))

        self.add_img_btn = CTkButton(option_fr, text="", image=img_table, width=100, height=100, corner_radius=5,
                                   border_color="green", border_width=1, command=lambda: self.show_file_dialog(),
                                   anchor="c", fg_color="white", hover_color="white")
        self.add_img_btn.grid(row=6, column=1, pady=entry_padding)

    def show_file_dialog(self):
        self.file_path = filedialog.askopenfilename(title="Chọn hình",
                                                    filetypes=(("jpeg", "*.jpg"), ("png", "*.png")))
        if self.file_path:
            try:
                # Mở hình ảnh
                with Image.open(self.file_path) as img:
                    if img.mode == "RGBA":
                        img = img.convert("RGB")
                    # Tạo thumbnail
                    thumbnail = img.copy()
                    thumbnail.thumbnail((100,100))
                    # Chuyển đổi thumbnail thành dạng bytes
                    with io.BytesIO() as output:
                        thumbnail.save(output, format="JPEG")  # Chọn định dạng hình ảnh tuỳ thích
                        self.thumbnail_bytes = output.getvalue()
                        image = ImageTk.PhotoImage(img.resize((100, 100)))
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
        else:
            self.product_page()



    def item_treeview_selected(self):
        selected_items = self.tv.selection()
        for item in selected_items:
            item = self.tv.item(item)
            self.product_name_var.set(item.get("values")[1])
            self.product_unit_var.set(item.get("values")[2])
            self.product_price_var.set(item.get("values")[3])
            self.product_quantity_var.set(item.get("values")[4])
            self.product_capacity_var.set(item.get("values")[5])
            self.product_alcohol_var.set(item.get("values")[6])
            self.product_type_var.set(item.get("values")[7])
            get_product_by_id = lambda id:next((item for item in self.__controller.products if item.id == id), None)
            produc_item = get_product_by_id(item.get("values")[0])
            if produc_item:
                image_decode = produc_item.image + b'=' * (-len(produc_item.image) % 4)
                de = base64.b64decode(image_decode)
                image = Image.open(io.BytesIO(de))
                photo = ImageTk.PhotoImage(image.resize((100, 100)))
                self.add_img_btn.configure(image=photo)
            print(item)

    def add_click(self):
        if self.__current_page == StatePage.Product:
            img = base64.b64encode(self.thumbnail_bytes)
            self.__controller.add_new_and_reload(name=self.product_name_var.get(),
                                                 price=self.product_price_var.get(),
                                                 unit=self.product_unit_var.get(),
                                                 quantity=self.product_quantity_var.get(),
                                                 capacity=self.product_capacity_var.get(),
                                                 alcohol=self.product_alcohol_var.get(),
                                                 productType=self.product_type_var.get(),
                                                 image=img)
            self.reload_treeview()
        else:
            self.__controller.add_discount()


    def update_click(self):
        if self.__current_page == StatePage.Product:
            selected_items = self.tv.selection()
            if not selected_items:
                messagebox.showwarning("Thông báo", "Vui lòng chọn dòng muốn chỉnh sửa.")
                return
            img = base64.b64encode(self.thumbnail_bytes)
            for item in selected_items:
                item_id = self.tv.item(item, "values")[0]
                self.__controller.update_and_reload(id=item_id,
                                                    name=self.product_name_var.get(),
                                                    price=self.product_price_var.get(),
                                                    unit=self.product_unit_var.get(),
                                                    quantity=self.product_quantity_var.get(),
                                                    capacity=self.product_capacity_var.get(),
                                                    alcohol=self.product_alcohol_var.get(),
                                                    product_type=self.product_type_var.get(),
                                                    image=img)
            self.reload_treeview()
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
                               values=(p.id, p.name, p.unit, p.price, p.quantity,
                                       p.capacity, p.alcohol, p.productType, p.createdDate, p.updatedDate))
