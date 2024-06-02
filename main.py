from ctypes import windll
import tkinter as tk
from login.login_controller import LoginController

if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)  # Improve quality on UI on windows
    root = tk.Tk()
    root.resizable(True, True)
    root.state('zoomed')  # Full screen
    root.iconbitmap('./assets/restaurant.ico')
    root.title("Restaurant Information")

    # App start here
    login_controller = LoginController()
    login_controller.open_page(root)

    root.mainloop()
