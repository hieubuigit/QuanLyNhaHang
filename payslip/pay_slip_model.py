from peewee import JOIN, fn

from entities.models import Payslip, User, Paygrade
from pay_grade.pay_grade_model import PayGradeModel
from share.utils import Utils


class PaySlipModel:
    def __init__(self):
        self.__pay_grade = PayGradeModel()

    def save(self, month, **data):
        # Save new payslip (Phiếu lương) into database
        if self.is_already_calculate_salary_this_month(month):
            return -1
        # if 'user_id' in data:
            # total_salary = self.calculate_salary(**data)
            # data['total_salary'] = total_salary
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
                                Payslip.updated_date, User.id)
                 .where(User.user_code.contains(conditions['user_id']) if conditions['user_id'] is not None else True)
                 .join(User, JOIN.RIGHT_OUTER, on=(Payslip.user == User.id))
                 .first())
        if query:
            return {
                'user_code': query.user.user_code,
                'full_name': f"{query.user.first_name} {query.user.last_name}",
                'gender': Utils.get_gender(query.user.gender),
                'user_name': query.user.user_name,
                'birth_date': query.user.birth_date,
                'identity': query.user.identity,
                'type_name': Utils.get_account_type_str(query.user.type),
                'type': query.user.type,
                'id': query.id,
                'hours': query.hours,
                'total_salary': query.total_salary,
                'created_date': query.created_date,
                'updated_date': query.updated_date,
                'user_id': query.user.id,
            }
        else:
            return None

    def is_already_calculate_salary_this_month(self, month: int):
        if 1 <= month <= 13:
            query = Payslip.select().where(Payslip.created_date.month == month)
            print(">>", query)
            if query is None:
                return True
        return False
