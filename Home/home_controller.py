import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from Home.home_View import HomeView
from Report.report_controller import ReportController


class HomeController:
    def __init__(self, root):
        super().__init__()
        view = HomeView(root, self)

    def nav_report_page(self, root):
        report = ReportController(root=root)


if __name__ == '__main__':
    root = ctk.CTk()
    root.resizable(True, True)
    root.state('zoomed')  # full screen
    root.title("Restaurant Information")
    home = HomeController(root)
    root.mainloop()

# style.theme_use('default') #('blue', 'alt', 'scidsand', 'classic', 'scidblue', 'scidmint', 'scidgreen', 'default', 'scidpink', 'aqua', 'scidgrey', 'scidpurple', 'clam')
