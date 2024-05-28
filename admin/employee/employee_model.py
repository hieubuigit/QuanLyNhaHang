import bcrypt
from peewee import *
from entities.models import User
from share.utils import Utils
import datetime

class EmployeeModel(Model):
    prefix_emp_code = "NV"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_employee_code(self):
        # Auto create employee id when create add new employee
        latest_user = (User.select().order_by(User.id.desc()).first())
        if latest_user.id:
            emp_id = f"{EmployeeModel.prefix_emp_code}{latest_user.id}"
            return emp_id
        return f"{EmployeeModel.prefix_emp_code}{1}"

    def add_new(self, **data):
        byte_password = bytes(data['password'], "utf-8")
        password = bcrypt.hashpw(byte_password, bcrypt.gensalt(rounds=10))
        data['password'] = password
        data['birth_date'] = Utils.format_date(data['birth_date'])
        data['income_date'] = Utils.format_date(data['income_date'])
        data['created_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = User(**data)
        result = user.save()
        return result

    def get_emp_by_id(self, id):
        user: User = User.select().where(User.id == id).first()
        return user

    def get_employee_list(self, **search_condition):
        # Get all employee list
        search_pattern = ""
        if "keyword" in search_condition and search_condition["keyword"] != "":
            search_pattern = search_condition["keyword"]
        data: list[User] = (User.select().where(search_pattern == "" or (fn.CONCAT(User.first_name, ' ', User.last_name).contains(search_pattern))
                                                or User.user_code.contains(search_pattern))
                            .order_by(User.first_name.desc()))
        emp_list = list()
        if data:
            for idx, user in enumerate(data):
                emp = list()
                emp.append(idx + 1)
                emp.append(user.user_code)
                emp.append(f"{user.first_name} {user.last_name}")
                emp.append(user.birth_date)
                emp.append(user.identity)
                emp.append(Utils.get_gender(user.gender))
                emp.append(user.income_date)
                emp.append(user.phone_number)
                emp.append(user.email)
                emp.append(user.address)
                emp.append(user.user_name)
                emp.append(Utils.get_status_account_name(user.status))
                emp.append(Utils.get_account_type_str(user.type))
                emp.append(user.created_date.strftime("%Y-%m-%d %H:%M:%S"))
                emp.append(user.id)
                emp_list.append(emp)
        return emp_list

    def update_by_id(self, id, new_data):
        new_data['birth_date'] = Utils.format_date(new_data['birth_date'])
        new_data['income_date'] = Utils.format_date(new_data['income_date'])
        new_data['updated_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = User.update(**new_data).where(User.id == id)
        return query.execute()

    def delete_by_id(self, id):
        query = User.delete().where(User.id == id)
        return query.execute()