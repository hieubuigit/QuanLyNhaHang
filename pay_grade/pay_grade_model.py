from entities.models import Paygrade, User
from share.utils import Utils


class PayGradeModel:
    def __init__(self):
        pass

    def save(self, **data):
        query = Paygrade(**data)
        return query.save()

    def delete(self, id):
        query = Paygrade.delete().where(Paygrade.id == id)
        return query.execute()

    def update(self, id, new_data):
        query = Paygrade.update(**new_data).where(Paygrade.id == id)
        return query.execute()

    def search(self, **conditions):
        # Get all pay grade of employee
        query: list[Paygrade] = Paygrade.select()
        data = list()
        if query:
            for idx, pg in enumerate(query):
                pay_grade_item = list()
                pay_grade_item.append(idx + 1)
                pay_grade_item.append(Utils.get_account_type_str(pg.type))
                pay_grade_item.append(pg.allowance)
                pay_grade_item.append(pg.pay_per_hours)
                pay_grade_item.append(pg.created_date.strftime("%Y-%m-%d %H:%M:%S"))
                pay_grade_item.append(pg.updated_date.strftime("%Y-%m-%d %H:%M:%S"))
                pay_grade_item.append(pg.id)
                data.append(pay_grade_item)
        return data

