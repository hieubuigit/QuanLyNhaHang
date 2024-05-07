
import tkinter as tk
from tkinter import ttk
from Home.home_View import HomeView


class HomeController:
    def __init__(self, root):
        super().__init__()
        view = HomeView(root)


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(True, True)
    root.state('zoomed')  # full screen
    root.title("Restaurant Information")

    home = HomeController(root)
    root.mainloop()