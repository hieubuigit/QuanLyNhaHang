import peewee

from Table_Order.menu_food import MenuFood
from WareHouse.product_model import Product
from database.connection import Connection


class MenuFoodController:
    def __init__(self, parent):
        self.__foods = []
        self.get_foods()
        view = MenuFood(parent, self)
    @property
    def foods(self):
        return self.__foods

    @foods.setter
    def foods(self, value):
        self.__foods = value

    def get_foods(self):
        try:
            Connection.db_handle.connect()
            rows = Product().select()
            self.__foods = rows
            print("Save bill success")
        except peewee.InternalError as px:
            print("Update bill failure")
            print(str(px))
        finally:
            Connection.db_handle.close()

    def update_quantity(self):
        pass
