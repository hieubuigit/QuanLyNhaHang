from ctypes import windll
import tkinter as tk

from login.login_view import LoginView

if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)  # Improve quality on UI on windows
    root = tk.Tk()
    root.resizable(True, True)
    root.state('zoomed')  # Full screen

    # App start here
    login = LoginView(root)

    root.mainloop()
