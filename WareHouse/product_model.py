from datetime import datetime

from peewee import Model, InternalError
from entities.models import database, Product


class ProductModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with database:
            database.create_tables([Product], safe=True)

    def get_products(self):
        try:
            pr = Product.table_exists()
            if not pr:
                Product.create_table()
            rows = Product.select()
            return rows
        except InternalError as px:
            print(str(px))

    def get_product_by_id(self, id):
        try:
            p = Product.get_or_none(Product.id == id)
            return p
        except InternalError as px:
            print(str(px))

    def save_product(self, name, price, unit, quantity, capacity, alcohol, product_type, image):
        try:
            row = Product(name=name, price=price, unit=unit, quantity=quantity, capacity=capacity, alcohol=alcohol,
                          productType=product_type, image=image, createdDate=datetime.now())
            row.save()
        except InternalError as px:
            print(str(px))

    def delete_product(self, product_id):
        try:
            product = Product.get_or_none(Product.id == product_id)
            if product:
                product.delete_instance()
            else:
                print(f"No record found with ID {product_id}")
        except InternalError as px:
            print(str(px))

    def update_product(self, id, name, price, unit, quantity, capacity, alcohol, product_type, image):
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
            product.updatedDate = datetime.now()
            product.save()
            print("Update table success")
        except InternalError as px:
            print("Update table failure")
            print(str(px))
