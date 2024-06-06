from peewee import JOIN, fn
from entities.models import Payslip, User, Paygrade
from pay_grade.pay_grade_model import PayGradeModel
from share.utils import Utils


class PaySlipModel:
    def __init__(self):
        self.__pay_grade = PayGradeModel()

    def save(self, **data):
        # Save new payslip (Phiếu lương) into database
        query = Payslip(**data)
        return query.save()

    def delete(self, id):
        query = Payslip.delete().where(Payslip.id == id)
        return query.execute()

    def update(self, id, new_data):
        query = Payslip.update(**new_data).where(Payslip.id == id)
        return query.execute()

    def get_all(self, **conditions):
        search_pattern = ''
        if "keyword" in conditions and conditions["keyword"] != "":
            search_pattern = conditions["keyword"]

        # Get all payslip of employee
        query = (Payslip.select(User.user_code, User.first_name, User.last_name, User.gender, User.user_name,
                                User.birth_date, User.identity, User.type,
                                Payslip.id, Payslip.hours, Payslip.total_salary, Payslip.created_date,
                                Payslip.updated_date, Payslip.pay_on_month, User.id)
                 .join(User)
                 .where(search_pattern == "" or (User.user_code.contains(search_pattern)
                                                 | (fn.CONCAT(User.first_name, ' ', User.last_name).contains(search_pattern))))
                 .order_by(Payslip.created_date))
        data = list()
        if query:
            for idx, psl in enumerate(query):
                pay_slip_item = list()
                pay_slip_item.append(idx + 1)
                pay_slip_item.append(psl.user.user_code)
                pay_slip_item.append(f"{psl.user.first_name} {psl.user.last_name}")
                pay_slip_item.append(psl.user.user_name)
                pay_slip_item.append(Utils.get_gender(psl.user.gender))
                pay_slip_item.append(psl.user.birth_date)
                pay_slip_item.append(psl.user.identity)
                pay_slip_item.append(Utils.get_account_type_str(psl.user.type))
                pay_slip_item.append(psl.id)
                pay_slip_item.append(psl.pay_on_month)
                pay_slip_item.append(psl.hours)
                pay_slip_item.append(psl.total_salary)
                if psl.created_date is not None:
                    pay_slip_item.append(psl.created_date.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    pay_slip_item.append('')
                if psl.updated_date is not None:
                    pay_slip_item.append(psl.updated_date.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    pay_slip_item.append('')
                pay_slip_item.append(psl.user.user_code)
                pay_slip_item.append(psl.id)

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
                                Payslip.id, Payslip.hours, Payslip.total_salary, Payslip.created_date, Payslip.pay_on_month,
                                Payslip.updated_date, User.id)
                 .where(User.user_code.contains(conditions['user_id']) if conditions['user_id'] is not None else True)
                 .join(User, JOIN.RIGHT_OUTER, on=(Payslip.user == User.id))
                 .first())

        # Get allowance
        allowance_by_type = Paygrade.select().where(Paygrade.type == query.user.type).first()
        allowance = 0
        if allowance_by_type:
            allowance = allowance_by_type.allowance

        if query:
            created_date = ""
            updated_date = ""
            if query.created_date is not None:
                created_date = query.created_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                created_date = ''
            if query.updated_date is not None:
                updated_date = query.updated_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                updated_date = ''
            return {
                'user_code': query.user.user_code,
                'full_name': f"{query.user.first_name} {query.user.last_name}",
                'gender': Utils.get_gender(query.user.gender),
                'user_name': query.user.user_name,
                'birth_date': query.user.birth_date,
                'identity': query.user.identity,
                'type_name': Utils.get_account_type_str(query.user.type),
                'type': query.user.type,
                'hours': query.hours,
                'pay_on_month': query.pay_on_month,
                'total_salary': query.total_salary,
                'created_date': created_date,
                'updated_date': updated_date,
                'user_id': query.user.id,
                'id': query.id,
                'allowance': allowance,
            }
        else:
            return None

    def is_already_calculate_salary_this_month(self, user_id, month_year: str):
        query = Payslip.select().where((Payslip.user == user_id) & (Payslip.pay_on_month == month_year)).first()
        if query:
            return True
        return False

    def get_all_nv(self):
        # Get all employee to fill data on combobox
        query = User.select(User.user_code).where(User.status == 1).order_by(User.user_name)
        user_code_list = []
        if query:
            for user in query:
                user_code_list.append(user.user_code)
        return user_code_list