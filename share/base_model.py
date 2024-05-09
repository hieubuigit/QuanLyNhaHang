from peewee import Model

from database.connection import Connection


class BaseModel(Model):
    class Meta:
        database = Connection.db_handle