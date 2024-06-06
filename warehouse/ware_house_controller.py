import datetime
from tkinter import messagebox
from peewee import fn, InternalError
from warehouse.discount_controller import DiscountController
from warehouse.product_model import ProductModel
from warehouse.ware_house_view import WareHouseView
from database.connection import Connection
from entities.models import Product


class WareHouseController:

    def __init__(self, root):
        self.__products = []
        self._product_model = ProductModel()
        self.get_data()
        view = WareHouseView(root, self)
        self.__discount_page = None

    @property
    def products(self):
        return self.__products

    def get_data(self):
        self.__products = []
        rows = self._product_model.get_products()
        if rows:
            self.__products.extend(rows)

    def search_product(self, key):
        self.__products = []
        try:
            rows = Product.select().where(fn.Lower(Product.name).contains(fn.Lower(key)))
            self.__products.extend(rows)
        except InternalError as px:
            print(str(px))

    def add_new_and_reload(self, id, name, price, unit, quantity, capacity, alcohol, productType, image):
        if self._product_model.get_product_by_id(id):
            messagebox.showinfo(message="Sản phẩm đã tồn tại")
            return
        self._product_model.save_product(name, price, unit, quantity, capacity, alcohol, productType, image)
        self.get_data()

    def delete_and_reload(self, id):
        self._product_model.delete_product(id)
        self.get_data()

    def update_and_reload(self, id, name, price, unit, quantity, capacity, alcohol, product_type, image):
        self._product_model.update_product(id, name, price, unit, quantity, capacity, alcohol, product_type, image)
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
