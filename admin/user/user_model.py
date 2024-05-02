from peewee import *
from datetime import date, datetime
from database.abc_common_db import abcCommonDb
from database.connection import Connection


class User(Model):
    id = PrimaryKeyField()
    userCode = CharField()
    firstName = CharField()
    lastName = CharField()
    birthDate = DateField()
    identity = CharField()
    gender = IntegerField()
    incomeDate = DateField()
    phoneNumber = CharField()
    email = CharField()
    address = CharField()
    # Fields for login account
    userName = CharField()
    password = CharField()
    status = IntegerField()
    type = IntegerField()
    createdDate = DateTimeField()
    updatedDate = DateTimeField()


class UserMapping:
    def __init__(self, **data):
        self.__id = 0
        self.__userCode = data['userCode']
        self.__firstName = data['firstName']
        self.__lastName = data['lastName']
        self.__birthDate = data['birthDate']
        self.__identity = data['identity']
        self.__gender = data['gender']
        self.__incomeDate = data['incomeDate']
        self.__phoneNumber = data['phoneNumber']
        self.__email = data['email']
        self.__address = data['address']

        # Fields for login account
        self.__userName = data['userName']
        self.__password = data['password']
        self.__status = data['status']
        self.__type = data['type']
        self.__createdDate = datetime.now()
        self.__updatedDate = None


class UserModel(abcCommonDb):
    USER_TBL_NAME = 'User'

    def __init__(self):
        super().__init__()
        # self.__controller = UserController()
        self.__connection = Connection()

    def get(self, **condition):
        sql = "GetAllUser"
        params = {**condition}
        pass

    def insert(self, insert_model):
        pass

    def update(self, id, update_model):
        pass

    def delete(self, id):
        pass

    def get_password_hash(self, user_name):
        sql = f"SELECT * FROM user where UserName = '{user_name}'"
        self.__connection.cursor.execute(sql)
        record = self.__connection.cursor.fetchone()
        return record[12]
