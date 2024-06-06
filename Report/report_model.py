from peewee import Model, InternalError

from entities.models import database, Billing, User, Table


class ReportModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with database:
            database.create_tables([Billing, Table], safe=True)

    def get_bills(self, start_date, end_date):
        try:
            results = Billing.select().where(Billing.createdDate.between(start_date, end_date)).order_by(
                Billing.createdDate.asc())
            return results
        except InternalError as px:
            print(str(px))

    def get_user_name(self, _id):
        try:
            user: User = User.get_or_none(User.id == _id)
            if user:
                return user.user_name
        except InternalError as px:
            print(str(px))
    def get_table_num(self, _id):
        try:
            t = Table.table_exists()
            if not t:
                Table.create_table()
            t: Table = Table.get_or_none(Table.id == _id)
            if t:
                return t.tableNum
        except InternalError as px:
            print(str(px))
