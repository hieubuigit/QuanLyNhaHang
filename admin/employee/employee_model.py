from database.abc_common_db import CommonDb

class EmployeeModel(CommonDb):
    def __init__(self, **kwargs: dict()):
        self.__emp_id = kwargs['emp_id']
        self.__first_name = kwargs['first_name']
        self.__last_name = kwargs['last_name']
        self.__birthday = kwargs['birthday']
        self.__gender = kwargs['gender']
        self.__phone_number = kwargs['phone_number']
        self.__email = kwargs['email']
        self.__basic_salary = kwargs['basic_salary']
        self.__address = kwargs['address']
        self.__material_status = kwargs['material_status']
        self.__avatar_url = kwargs['avatar_url']
        self.__created_date = kwargs['created_date']
        self.__updated_date = kwargs['updated_date']

    @property
    def emp_id(self):
        return self.__emp_id

    @emp_id.setter
    def emp_id(self, emp_id):
        self.__emp_id = emp_id

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        self.__last_name = last_name

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        self.__first_name = first_name

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        self.__birthday = birthday

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, gender):
        self.__gender = gender

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        self.__phone_number = phone_number

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def basic_salary(self):
        return self.__basic_salary

    @basic_salary.setter
    def basic_salary(self, basic_salary):
        self.__basic_salary = basic_salary

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address

    @property
    def material_status(self):
        return self.__material_status

    @material_status.setter
    def material_status(self, material_status):
        self.__material_status = material_status

    @property
    def avatar_url(self):
        return self.__avatar_url

    @avatar_url.setter
    def avatar_url(self, avatar_url):
        self.__avatar_url = avatar_url

    @property
    def created_date(self):
        return self.__created_date

    @created_date.setter
    def created_date(self, created_date):
        self.__created_date = created_date

    @property
    def updated_date(self):
        return self.__updated_date

    @updated_date.setter
    def updated_date(self, updated_date):
        self.__updated_date = updated_date
