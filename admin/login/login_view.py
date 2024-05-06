from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as tkMessageBox
import os
from PIL import Image, ImageTk

from admin.login.login_controller import LoginController


class LoginView:
    def __init__(self, container):
        self.__controller = LoginController()
        # self.__user = UserMapping()
        self.init_view(container)

    def init_view(self, container):

        user_name = tk.StringVar()
        password = tk.StringVar()

        login_form = ttk.Frame(container, width=700)

        heading = ttk.Label(login_form, text="Đăng nhập", font=('', 20, 'bold'))
        heading.grid(column=0, row=0, padx=5, pady=5)

        # Login logo
        try:
            photo = ImageTk.PhotoImage(Image.open('../../assets/password.png').resize((100, 100)))
            photo_lbl = ttk.Label(login_form, image=photo)
            photo_lbl.image = photo
            photo_lbl.grid(column=0, row=1, sticky='n', padx=5, pady=5)
        except Exception as e:
            print("[!] Exception: ", e)

        # Username field
        username_lbl = ttk.Label(login_form, text="Tên người dùng: ", font=('', 11))
        username_lbl.grid(column=0, row=2, sticky='we', padx=5, pady=5)
        username_ent = ttk.Entry(master=login_form, textvariable=user_name)
        username_ent.grid(column=0, row=3, sticky='we', padx=5, pady=5, ipadx=10, ipady=5)

        # Password field
        password_lbl = ttk.Label(login_form, text="Mật khẩu: ", font=('', 11))
        password_lbl.grid(column=0, row=4, sticky='we', padx=5, pady=5)
        password_ent = ttk.Entry(master=login_form, textvariable=password, show="*")
        password_ent.grid(column=0, row=5, stick='we', padx=5, pady=5, ipadx=10, ipady=5)

        # Login button
        # login_ico = tk.PhotoImage(file='../../assets/password.png', width=50, height=50)
        login_ico = ImageTk.PhotoImage(Image.open('../../assets/arrow.png').resize((30, 30)))
        login_btn = tk.Button(master=login_form, text='Đăng nhập', width=10, bg='#9c9c9c', fg="white", font=('', 11), image=login_ico, compound='left', padx=5)
        login_btn.image = login_ico
        login_btn.bind('<Button>', lambda event: self.on_login_click(event, user_name.get(), password_ent.get()))
        login_btn.grid(column=0, row=6, sticky='ew', pady=20, padx=20)

        login_form.place(relx=0.5, rely=0.5, anchor='center')

    def on_login_click(self, event, username, password):
        if username == "" or password == "":
            tkMessageBox.showinfo("Cảnh báo", "Cập nhật đầy đủ thông tin trước khi đăng nhập!")
        else:
            self.__controller.login(username, password)



