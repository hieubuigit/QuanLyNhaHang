
from peewee import *
from entities.models import Table
class TableModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_data(self):
        if Table.table_exists():
            return Table.select()


