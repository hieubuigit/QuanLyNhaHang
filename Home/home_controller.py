import tkinter as tk
from Report.report_controller import ReportController
from Home.home_view import HomeView


class HomeController:
    def __init__(self, app_root):
        view = HomeView(app_root, self)

    def nav_report_page(self, parent):
        report = ReportController(root=parent)

if __name__ == '__main__':
    root = tk.Tk()
    root.iconbitmap('../assets/restaurant.ico')
    root.resizable(True, True)
    root.state('zoomed')  # full screen
    root.title("Quản lý nhà hàng")
    home = HomeController(root)
    root.mainloop()

# style.theme_use('default') #('blue', 'alt', 'scidsand', 'classic', 'scidblue', 'scidmint', 'scidgreen', 'default', 'scidpink', 'aqua', 'scidgrey', 'scidpurple', 'clam')
