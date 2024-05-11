from datetime import datetime

import peewee
from Bill.bill_model import Billing
from Bill.bill_view import BillView
import tkinter as tk
from database.connection import Connection

class BillController:
    def __init__(self, window):
        view = BillView(window, self)

    def get_data(self, by_date):
        bills = []
        try:
            Connection.db_handle.connect()
            results = Billing.select().where(Billing.createdDate.year == by_date.year
                                             and Billing.createdDate.month == by_date.month
                                             and Billing.createdDate.day == by_date.day)
            bills.extend(results)
        except peewee.InternalError as px:
            print(str(px))
        finally:
            Connection.db_handle.close()
        return bills

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(True, True)
    root.state('zoomed')  # full screen
    root.title("Restaurant BILL")
    home = BillController(root)
    root.mainloop()
