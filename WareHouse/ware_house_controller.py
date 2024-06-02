import datetime
from tkinter import messagebox
import peewee
from WareHouse.discount_controller import DiscountController
from WareHouse.ware_house_view import WareHouseView
from database.connection import Connection
from entities.models import Product


class WareHouseController:
    def __init__(self, root):
        self.__products = []
        self.get_data()
        view = WareHouseView(root, self)

    @property
    def products(self):
        return self.__products

    def get_data(self):
        self.__products = []
        try:
            Connection.db_handle.connect()
            pr = Product.table_exists()
            if not pr:
                Product.create_table()
            rows = Product.select()
            self.__products.extend(rows)
        except peewee.InternalError as px:
            print(str(px))
        finally:
            Connection.db_handle.close()
    def save_data_to_db(self, name, price, unit, quantity, capacity, alcohol, product_type, image):
        try:
            Connection.db_handle.connect()
            pr = Product.table_exists()
            if not pr:
                Connection.db_handle.create_tables([Product], safe=True)
            row = Product(name=name, price=price, unit=unit, quantity=quantity, capacity=capacity, alcohol=alcohol,

                          productType=product_type, image=image, createdDate=datetime.datetime.now())

            row.save()

            messagebox.showinfo("Thông báo", "Thêm sản phẩm thành công")

        except peewee.InternalError as px:
            messagebox.showinfo("Thông báo", "Thêm sản phẩm thất bại. Vui lòng thử lại.")
            print(str(px))
        finally:
            Connection.db_handle.close()

    def __delete_product(self, product_id):
        try:
            Connection.db_handle.connect()
            product = Product.get_or_none(Product.id == product_id)
            if product:
                product.delete_instance()
                messagebox.showinfo("Thông báo", "Xóa bàn thành công")
            else:
                print(f"No record found with ID {product_id}")
                messagebox.showinfo("Thông báo", "Xóa bàn thất bại")
        except peewee.InternalError as px:
            print(str(px))
        finally:
            Connection.db_handle.close()

    def __update_product_to_db(self, id, name, price, unit, quantity, capacity, alcohol, product_type, image):
        try:
            Connection.db_handle.connect()
            product = Product.get(Product.id == id)
            product.name = name
            product.price = price
            product.unit = unit
            product.quantity = quantity
            product.capacity = capacity
            product.alcohol = alcohol
            product.productType = product_type
            product.image = image
            product.updatedDate = datetime.datetime.now()
            product.save()
            print("Update table success")
        except peewee.InternalError as px:
            print("Update table failure")
            print(str(px))
        finally:
            Connection.db_handle.close()
    def add_new_and_reload(self, name, price, unit, quantity, capacity, alcohol, productType, image):
        self.save_data_to_db(name, price, unit, quantity, capacity, alcohol, productType, image)
        self.get_data()

    def delete_and_reload(self, id):
        self.__delete_product(id)
        self.get_data()

    def update_and_reload(self, id, name, price, unit, quantity, capacity, alcohol, product_type, image):
        self.__update_product_to_db(id, name, price, unit, quantity, capacity, alcohol, product_type, image)
        self.get_data()

    def nav_discount_page(self, root):
        self._discount_page = DiscountController(root)

    def add_discount(self):
        self._discount_page.add_new_and_reload()

    def delete_row_discount(self):
        self._discount_page.delete_and_reload()

    def update_row_discount(self):
        self._discount_page.update_and_reload()

