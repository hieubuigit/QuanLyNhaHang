from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from PIL import Image, ImageTk
from ctypes import windll
import customtkinter as ctk

from admin.login.login_controller import LoginController
from share.utils import Utils


class LoginView:
    def __init__(self, container):
        self.init_view(container)
        self.__controller = LoginController()

    def init_view(self, container):
        #Left column
        try:
            left_col = ctk.CTkFrame(container, fg_color="#fff")
            building_img = ctk.CTkImage(light_image=Image.open('../../assets/view-building-with-cartoon-style-architecture.jpg'), dark_image=Image.open('../../assets/view-building-with-cartoon-style-architecture.jpg'), size=(450, 600))
            building_lbl = ctk.CTkLabel(master=left_col, text="", image=building_img)
            building_lbl.image = building_img
            building_lbl.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
            left_col.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        except Exception as e:
            print("[!] Exception: ", e)

        # Right column
        login_form = ctk.CTkFrame(container, fg_color="#3224ff")
        heading = ctk.CTkLabel(login_form, text="Đăng nhập", font=('', 50, 'bold'), justify='center', text_color="#fff", pady=50)
        heading.pack(side=tk.TOP, fill=tk.BOTH)

        try:
            photo = ctk.CTkImage(light_image=Image.open('../../assets/password.png'), dark_image=Image.open('../../assets/password.png'), size=(100, 100))
            photo_lbl = ctk.CTkLabel(master=login_form, text="", image=photo)
            photo_lbl.image = photo
            photo_lbl.pack(side=tk.TOP, fill=tk.BOTH, pady=30)
        except Exception as e:
            print("[!] Exception: ", e)

        # Username field
        group_item_1 = ctk.CTkFrame(login_form, fg_color="#3224ff")
        username_lbl = ctk.CTkLabel(group_item_1, text="Tên người dùng: ", font=('', 14, 'bold'), justify='left', text_color="#fff", width=100)
        username_lbl.pack(**Utils.pack_control_item)
        username_ent = ctk.CTkEntry(master=group_item_1, placeholder_text="Nhập tên người dùng", width=300)
        username_ent.pack(**Utils.pack_control_item)
        group_item_1.pack(side=tk.TOP, expand=tk.NO)

        # Password field
        group_item_2 = ctk.CTkFrame(login_form, fg_color="#3224ff")
        password_lbl = ctk.CTkLabel(group_item_2, text="Mật khẩu: ", font=('', 14, 'bold'), justify='left', text_color="#fff", width=100)
        password_lbl.pack(**Utils.pack_control_item)
        password_ent = ctk.CTkEntry(master=group_item_2, placeholder_text="Nhập mật khẩu", show="*", width=300)
        password_ent.pack(**Utils.pack_control_item)
        group_item_2.pack(side=tk.TOP, expand=tk.NO)

        # Login button
        my_image = ctk.CTkImage(light_image=Image.open('../../assets/arrow.png'), dark_image=Image.open('../../assets/arrow.png'), size=(20, 20))
        login_btn = ctk.CTkButton(master=login_form, text='Đăng nhập', width=10, fg_color='red', text_color="white", font=('', 20, 'bold'), image=my_image, compound='left',
                                  command=lambda: self.on_login_click(username_ent.get(), password_ent.get()))
        login_btn.pack(side=tk.TOP, fill='none', expand=tk.NO, pady=50)
        login_form.pack(side='left', expand=tk.YES, fill=tk.BOTH)

    def on_login_click(self, username, password):
        if username == "" or password == "":
            tkMessageBox.showinfo("Cảnh báo", "Cập nhật đầy đủ thông tin trước khi đăng nhập!")
        else:
            self.__controller.login(username, password)

if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    root.state('zoomed')  # full screen
    root.resizable(True, True)
    root.iconbitmap('../../assets/restaurant.ico')
    root.title("Restaurant Information")
    view = LoginView(root)
    root.mainloop()
