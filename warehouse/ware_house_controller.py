import datetime
from tkinter import messagebox
from peewee import fn, InternalError
from warehouse.discount_controller import DiscountController
from warehouse.ware_house_view import WareHouseView
from database.connection import Connection
from entities.models import Product


class WareHouseController:

    def __init__(self, root):
        self.__products = []
        self.get_data()
        view = WareHouseView(root, self)
        self.__discount_page = None

    @property
    def products(self):
        return self.__products

    def get_data(self):
        self.__products = []
        try:
            pr = Product.table_exists()
            if not pr:
                Product.create_table()
            rows = Product.select()
            self.__products.extend(rows)
        except InternalError as px:
            print(str(px))

    def save_data_to_db(self,id,  name, price, unit, quantity, capacity, alcohol, product_type, image):
        try:
            p = Product.get_or_none(Product.id == id)
            if p:
                messagebox.showinfo(message="Sản phẩm đã tồn tại")
                return
            row = Product(name=name, price=price, unit=unit, quantity=quantity, capacity=capacity, alcohol=alcohol,

                          productType=product_type, image=image, createdDate=datetime.datetime.now())
            row.save()
        except InternalError as px:
            print(str(px))


    def __delete_product(self, product_id):
        try:
            product = Product.get_or_none(Product.id == product_id)
            if product:
                product.delete_instance()
            else:
                print(f"No record found with ID {product_id}")
        except InternalError as px:
            print(str(px))


    def __update_product_to_db(self, id, name, price, unit, quantity, capacity, alcohol, product_type, image):
        try:
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
        except InternalError as px:
            print("Update table failure")
            print(str(px))

    def search_product(self, key):
        self.__products = []
        try:
            rows = Product.select().where(fn.Lower(Product.name).contains(fn.Lower(key)))
            self.__products.extend(rows)
        except InternalError as px:
            print(str(px))
    def add_new_and_reload(self,id, name, price, unit, quantity, capacity, alcohol, productType, image):
        self.save_data_to_db(id, name, price, unit, quantity, capacity, alcohol, productType, image)
        self.get_data()

    def delete_and_reload(self, id):
        self.__delete_product(id)
        self.get_data()

    def update_and_reload(self, id, name, price, unit, quantity, capacity, alcohol, product_type, image):
        self.__update_product_to_db(id, name, price, unit, quantity, capacity, alcohol, product_type, image)
        self.get_data()

    def nav_discount_page(self, root):
        self.__discount_page = DiscountController(root)

    def add_discount(self):
        self.__discount_page.add_new_and_reload()

    def delete_row_discount(self):
        self.__discount_page.delete_and_reload()

    def update_row_discount(self):
        self.__discount_page.update_and_reload()

    def search_discount(self, key):
        self.__discount_page.search_discount(key)

