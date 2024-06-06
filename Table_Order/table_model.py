from datetime import datetime

from peewee import Model, InternalError
from entities.models import Table, Discount, Billing, User, database
from share.common_config import UserType, TableType, BillType, BillStatus, StatusTable
from share.utils import Utils


class TableModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with database:
            database.create_tables([Table, Billing, Discount], safe=True)

    def get_tables(self):
        try:
            rows: [Table] = Table.select()
            return rows
        except InternalError as px:
            print(str(px))

    def add_new_table(self, table_num, seat_num, status):
        try:
            row_table = Table(tableNum=table_num, seatNum=seat_num, status=status, createdDate=datetime.now())
            row_table.save()
        except InternalError as px:
            print(str(px))

    def get_table_by_table_num(self, table_num):
        try:
            table = Table.get_or_none(Table.tableNum == table_num)
            return table
        except InternalError as px:
            print(str(px))

    def update_table(self, id, table_num, seat_num, status):
        try:
            table = Table.get_or_none(Table.tableNum == table_num, Table.id != id)
            if table:
                return None
            table = Table.get(Table.id == id)
            table.tableNum = table_num
            table.seatNum = seat_num
            table.status = status
            table.updatedDate = datetime.now()
            table.save()
            return 1
        except InternalError as px:
            print(str(px))

    def update_table_status(self, id_table, status):
        try:
            table = Table.get(Table.id == id_table)
            table.status = status
            table.save()
        except InternalError as px:
            print(str(px))

    def delete_table(self, table_id):
        try:
            table = Table.get_or_none(Table.id == table_id)
            if table:
                table.delete_instance()
                return 1
        except InternalError as px:
            print(str(px))

    def create_bill_by_table(self, id_table, id_user):
        try:
            user = User.get(User.id == id_user)
            table = Table.get(Table.id == id_table)

            b = Billing()
            b.tableId = table
            b.userId = user
            b.type = BillType.REVENUE.value[0]
            b.status = BillStatus.UNPAID.value
            b.createdDate = datetime.now()
            b.save()
            return 1
        except InternalError as px:
            print(str(px))

    def is_my_bill(self, table_id):
        try:
            t: Table = Table.get_or_none(Table.id == table_id)
            if t.status == StatusTable.DISABLED.value[0]:
                b: Billing = Billing.select(Billing, Table, User).join(Table).switch(Billing).join(User).where(
                    (Billing.tableId == table_id) & (Billing.userId == Utils.user_profile["id"])).get_or_none()
                return b
        except InternalError as px:
            print(str(px))
