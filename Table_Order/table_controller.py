import tkinter as tk
from Table_Order.table_view import TableView


class TableController(tk.Frame):
    def __init__(self, window):
        super().__init__()
        view = TableView(window)


# if __name__ == '__main__':
#     root = tk.Tk()
#     root.resizable(True, True)
#     root.state('zoomed')  # full screen
#     root.title("Restaurant Information")
#     home = TableController(root)
#     root.mainloop()