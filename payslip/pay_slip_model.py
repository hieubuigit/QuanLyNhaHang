from peewee import JOIN

from entities.models import Payslip, User, Paygrade
from pay_grade.pay_grade_model import PayGradeModel
from share.utils import Utils


class PaySlipModel:
    def __init__(self):
        self.__pay_grade = PayGradeModel()

    def save(self, **data):
        # Save new payslip (Phiếu lương) into database
        if 'user_code' in data:
            total_salary = self.calculate_salary(**data)
            data['total_salary'] = total_salary
        query = Payslip(**data)
        return query.save()

    def delete(self, id):
        query = Payslip.delete().where(Payslip.id == id)
        return query.execute()

    def update(self, id, new_data):
        query = Payslip.update(**new_data).where(Payslip.id == id)
        return query.execute()

    def get_all(self, **conditions):
        # Get all payslip of employee
        query = (Payslip.select(User.user_code, User.first_name, User.last_name, User.gender, User.user_name,
                                User.birth_date, User.identity, User.type,
                                Payslip.id, Payslip.hours, Payslip.total_salary, Payslip.created_date,
                                Payslip.updated_date, User.id.alias('user_id'))
                 .join(User)
                 .order_by(Payslip.created_date))
        data = list()
        if query:
            for idx, psl in enumerate(query):
                pay_slip_item = list()
                pay_slip_item.append(idx + 1)
                pay_slip_item.append(psl.user_code)
                pay_slip_item.append(f"{psl.first_name} {psl.last_name}")
                pay_slip_item.append(psl.user_name)
                pay_slip_item.append(Utils.get_gender(psl.gender))
                pay_slip_item.append(psl.birth_date)
                pay_slip_item.append(psl.identity)
                pay_slip_item.append(Utils.get_account_type_str(psl.type))
                pay_slip_item.append(psl.id)
                pay_slip_item.append(psl.hours)
                pay_slip_item.append(psl.total_salary)
                pay_slip_item.append(psl.created_date.strftime("%Y-%m-%d %H:%M:%S"))
                pay_slip_item.append(psl.updated_date.strftime("%Y-%m-%d %H:%M:%S"))
                pay_slip_item.append(psl.user_id)

                data.append(pay_slip_item)
        return data

    def calculate_salary(self, **data):
        if 'type' in data and 'hours' in data:
            pay_grade_by_type: Paygrade = Paygrade.select().where(Paygrade.type == data['type']).first()
            if pay_grade_by_type:
                total_salary = data['hours'] * pay_grade_by_type.pay_per_hours + pay_grade_by_type.allowance
                return total_salary
        return 0

    def get_pay_slip_by_userid(self, conditions: dict):
        # Get on pay slip by user id
        query = (Payslip.select(User.user_code, User.first_name, User.last_name, User.gender, User.user_name,
                                User.birth_date, User.identity, User.type,
                                Payslip.id, Payslip.hours, Payslip.total_salary, Payslip.created_date,
                                Payslip.updated_date, User.id.alias('user_id'))
                 .where(User.user_code.contains(conditions['user_id']) if conditions['user_id'] is not None else True)
                 .join(User, JOIN.LEFT_OUTER, on=(User.id == Payslip.user))
                 .first())
        if query:
            print(
            f"User Code: {query.user_code}, First Name: {query.first_name}, Last Name: {query.last_name}, Gender: {query.gender}, "
            f"Username: {query.user_name}, Birth Date: {query.birth_date}, Identity: {query.identity}, Type: {query.type}, "
            f"Payslip ID: {query.id}, Hours: {query.hours}, Total Salary: {query.total_salary}, Created Date: {query.created_date}, "
            f"Updated Date: {query.updated_date}, User ID: {query.user_id}")
        else:
            print("No data")

        return query

    def is_already_calculate_salary_this_month(self):
        # query = Payslip.select().where(Payslip.created_date)
        pass
