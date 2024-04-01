from database.common_db import CommonDb

class EmployeeModel(CommonDb):
    def __init__(self, emp_id, first_name, last_name, birthday, gender, phone_number, email, basic_salary, address, material_status, avatar_url, created_date, updated_date):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.phone_number = phone_number
        self.email = email
        self.basic_salary = basic_salary
        self.address = address
        self.material_status = material_status
        self.avatar_url = avatar_url
        self.created_date = created_date
        self.updated_date = updated_date