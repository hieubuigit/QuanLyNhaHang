from peewee import *
from datetime import datetime
from entities.models import *


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


class LoginModel(Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_user_by_user_name(self, user_name):
        query: User = User.get(User.user_name == user_name)
        return query

    def is_exist(self, user_name):
        return User.select().where(User.user_name == user_name).exists()
