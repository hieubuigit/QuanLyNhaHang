import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from Home.tab_bar_view import TabBarView
from employee_view import EmployeeView


class HomeView(tk.Tk):
    path_assets = "{path_assets}".format(path_assets=os.getcwd().replace("Home", "assets"))
    def __init__(self):
        super().__init__()
        home_fr = tk.Frame(self)
        tab_bar = TabBarView(self)
        tab_bar.pack()
        home_fr.pack(fill=tk.BOTH, expand=1)


if __name__ == "__main__":
    app = HomeView()
    app.resizable(True, True)
    app.state('zoomed')
    app.mainloop()