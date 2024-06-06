import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
from PIL import Image
# from ctypes import windll
import customtkinter as ctk
from home.home_controller import HomeController
from login.login_controller import LoginController
from entities.models import User, database
from share.utils import Utils


class LoginView:
    def __init__(self, container):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", background="DodgerBlue1", forceground="white", font=("TkDefaultFont", 12))
        # windll.shcore.SetProcessDpiAwareness(1)

        self.__parent = container
        self.__controller = LoginController()
        self.__login_page = ctk.CTkFrame(container)
        self.init_view(self.__login_page)

    def init_view(self, parent):
        #Left column
        try:
            left_col = ctk.CTkFrame(parent, fg_color="#fff")
            building_img = ctk.CTkImage(light_image=Image.open('../assets/view-building-with-cartoon-style-architecture.jpg'),
                dark_image=Image.open('../assets/view-building-with-cartoon-style-architecture.jpg'), size=(450, 600))
            building_lbl = ctk.CTkLabel(master=left_col, text="", image=building_img)
            building_lbl.image = building_img
            building_lbl.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
            left_col.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        except Exception as e:
            print("[!] Exception: ", e)

        # Right column
        login_form = ctk.CTkFrame(parent, fg_color=Utils.BLUE)
        wrap_controls = ctk.CTkFrame(login_form, fg_color=Utils.WHITE)

        heading = ctk.CTkLabel(wrap_controls, text="Đăng nhập", font=('', 50, 'bold'), justify='center', text_color=Utils.BLUE, pady=50)
        heading.pack(side=tk.TOP, fill=tk.BOTH)

        try:
            photo = ctk.CTkImage(light_image=Image.open('../assets/profile.png'), dark_image=Image.open(
                '../assets/profile.png'), size=(100, 100))
            photo_lbl = ctk.CTkLabel(master=wrap_controls, text="", image=photo)
            photo_lbl.image = photo
            photo_lbl.pack(side=tk.TOP, fill=tk.BOTH, pady=30)
        except Exception as e:
            print("[!] Exception: ", e)

        group_item = ctk.CTkFrame(wrap_controls, fg_color=Utils.WHITE)
        group_item.columnconfigure(0, weight=1)
        group_item.columnconfigure(1, weight=2)

        # Username field
        username_lbl = ctk.CTkLabel(group_item, text="Tên người dùng: ", font=('', 14, 'bold'), text_color=Utils.BLUE)
        username_lbl.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        username_ent = ctk.CTkEntry(master=group_item, placeholder_text="Nhập tên người dùng", width=200, fg_color=Utils.WHITE, text_color=Utils.BLACK)
        username_ent.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Password field
        password_lbl = ctk.CTkLabel(group_item, text="Mật khẩu: ", font=('', 14, 'bold'), text_color=Utils.BLUE)
        password_lbl.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        password_ent = ctk.CTkEntry(master=group_item, placeholder_text="Nhập mật khẩu", show="*", fg_color=Utils.WHITE, text_color=Utils.BLACK, width=200)
        password_ent.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        group_item.pack(side=tk.TOP, anchor="center", expand=tk.YES)

        # Login button
        my_image = ctk.CTkImage(light_image=Image.open('../assets/arrow.png'), dark_image=Image.open(
            '../assets/arrow.png'), size=(20, 20))
        login_btn = ctk.CTkButton(master=wrap_controls, text='Đăng nhập', width=10, fg_color=Utils.BLUE, text_color="white", font=('', 18, 'bold'), image=my_image, compound='left',
                                  command=lambda: self.on_login_click(username_ent.get(), password_ent.get()))
        login_btn.pack(side=tk.TOP, fill='none', expand=tk.NO, pady=30)
        wrap_controls.pack(side=tk.TOP, expand=tk.YES, padx=50, pady=50, ipadx=20)
        login_form.pack(side='left', expand=tk.YES, fill=tk.BOTH)
        parent.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

    def on_login_click(self, username, password):
        # Catch event login button click
        user: User
        if username == "" or password == "":
            tkMessageBox.showinfo("Cảnh báo", "Cập nhật đầy đủ thông tin trước khi đăng nhập!")
        else:
            user = self.__controller.login(username, password)
            if user is None:
                return
            self.__login_page.pack_forget()
            database.close()
            homepage = HomeController(self.__parent)


if __name__ == '__main__':
    # windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    root.state('zoomed')  # full screen
    root.resizable(True, True)
    root.iconbitmap('../assets/restaurant.ico')
    root.title("Restaurant Information")

    view = LoginView(root)
    root.mainloop()
