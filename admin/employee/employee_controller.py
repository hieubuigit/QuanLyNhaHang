from employee_model import EmployeeModel
from entities.models import User


class EmployeeController:
    def __init__(self):
        self.__emp_model = EmployeeModel()

    def get_list(self, **search_condition):
        try:
            data = self.__emp_model.get_employee_list(**search_condition)
            return data
        except Exception as es:
            print(es)

    def save(self, **data):
        try:
            saveResult = self.__emp_model.add_new(**data)
            return saveResult
        except Exception as es:
            print(es)

    def delete(self, id):
        pass

    def get_new_emp_id(self):
        try:
            return self.__emp_model.create_employee_code()
        except Exception as e:
            print(e)

    def get_emp_by_id(self, id):
        try:
            return self.__emp_model.get_emp_by_id(id)
        except Exception as e:
            print(e)