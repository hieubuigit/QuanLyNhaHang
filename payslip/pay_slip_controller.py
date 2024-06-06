from employee.employee_model import EmployeeModel
from payslip.pay_slip_model import PaySlipModel


class PaySlipController:
    def __init__(self):
        self.__pay_slip_model = PaySlipModel()
        self.__user_model = EmployeeModel()

    def add_new(self, **new_data):
        try:
            # Get employee info by use id
            user = self.__user_model.get_emp_by_id(new_data['user_id'])
            if user is not None:
                new_data.pop('user_id')
                new_data['user'] = user
            save_result = self.__pay_slip_model.save(**new_data)
            return save_result
        except Exception as ex:
            print(ex)

    def delete_by_id(self, id):
        try:
            result = self.__pay_slip_model.delete(id)
            return result
        except Exception as ex:
            print(ex)

    def get_all(self, **search_conditions):
        try:
            data = self.__pay_slip_model.get_all(**search_conditions)
            return data
        except Exception as ex:
            print(ex)

    def update_by_id(self, id, new_data):
        try:
            if 'user_id' in new_data:
                new_data.pop('user_id')
            save_result = self.__pay_slip_model.update(id, new_data)
            if save_result > 0:
                return 1
            else:
                return 0
        except Exception as e:
            print("[!Exc:", e)
            return 0

    def get_pay_slip_by_user_id(self, user_id):
        try:
            data = self.__pay_slip_model.get_pay_slip_by_userid({'user_id': user_id})
            return data
        except Exception as e:
            print("[!Exc:", e)
            return 0

    def calculate_salary(self, data: dict):
        try:
            result = self.__pay_slip_model.calculate_salary(**data)
            return result
        except Exception as e:
            print("[!Exc:", e)
            return 0

    def is_already_calculate_salary(self, user_id, month_year):
        try:
            result = self.__pay_slip_model.is_already_calculate_salary_this_month(user_id, month_year)
            return result
        except Exception as e:
            print("[!Exc:", e)
            return 0

    def get_employee_combobox(self):
        try:
            result = self.__pay_slip_model.get_all_nv()
            return result
        except Exception as e:
            print("[!Exc:", e)

