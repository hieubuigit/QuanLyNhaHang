import tkinter as tk
import tkinter.messagebox as tkMessageBox
from PIL import Image
from ctypes import windll
import customtkinter as ctk

from Home.home_View import HomeView
from admin.login.login_controller import LoginController
from admin.tab_controls.tab_controls import TabControls
from entities.models import User
from share.utils import Utils


class LoginView:
    def __init__(self, container):
        self.__parent = container
        self.__controller = LoginController()
        self.__login_page = ctk.CTkFrame(container)
        self.init_view(self.__login_page)

    def init_view(self, parent):
        #Left column
        try:
            left_col = ctk.CTkFrame(parent, fg_color="#fff")
            building_img = ctk.CTkImage(light_image=Image.open('../../assets/view-building-with-cartoon-style-architecture.jpg'), dark_image=Image.open('../../assets/view-building-with-cartoon-style-architecture.jpg'), size=(450, 600))
            building_lbl = ctk.CTkLabel(master=left_col, text="", image=building_img)
            building_lbl.image = building_img
            building_lbl.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
            left_col.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        except Exception as e:
            print("[!] Exception: ", e)

        # Right column
        login_form = ctk.CTkFrame(parent, fg_color=Utils.BLUE)
        wrap_controls = ctk.CTkFrame(login_form, fg_color=Utils.WHITE, corner_radius=8)

        heading = ctk.CTkLabel(wrap_controls, text="Đăng nhập", font=('', 50, 'bold'), justify='center', text_color=Utils.BLUE, pady=50)
        heading.pack(side=tk.TOP, fill=tk.BOTH)

        try:
            photo = ctk.CTkImage(light_image=Image.open('../../assets/profile.png'), dark_image=Image.open('../../assets/profile.png'), size=(100, 100))
            photo_lbl = ctk.CTkLabel(master=wrap_controls, text="", image=photo)
            photo_lbl.image = photo
            photo_lbl.pack(side=tk.TOP, fill=tk.BOTH, pady=30)
        except Exception as e:
            print("[!] Exception: ", e)

        # Username field
        group_item_1 = ctk.CTkFrame(wrap_controls, fg_color=Utils.WHITE)
        username_lbl = ctk.CTkLabel(group_item_1, text="Tên người dùng: ", font=('', 14, 'bold'), text_color=Utils.BLUE, width=90, anchor="w")
        username_lbl.pack(**Utils.pack_control_item)
        username_ent = ctk.CTkEntry(master=group_item_1, placeholder_text="Nhập tên người dùng", width=300, fg_color=Utils.WHITE, text_color=Utils.BLACK)
        username_ent.pack(**Utils.pack_control_item)
        group_item_1.pack(side=tk.TOP, anchor="w", expand=tk.NO)

        # Password field
        group_item_2 = ctk.CTkFrame(wrap_controls, fg_color=Utils.WHITE)
        password_lbl = ctk.CTkLabel(group_item_2, text="Mật khẩu: ", font=('', 14, 'bold'), text_color=Utils.BLUE, width=90, anchor="w")
        password_lbl.pack(**Utils.pack_control_item)
        password_ent = ctk.CTkEntry(master=group_item_2, placeholder_text="Nhập mật khẩu", show="*", width=300, fg_color=Utils.WHITE, text_color=Utils.BLACK)
        password_ent.pack(**Utils.pack_control_item)
        group_item_2.pack(side=tk.TOP, anchor="w", expand=tk.NO)

        # Login button
        my_image = ctk.CTkImage(light_image=Image.open('../../assets/arrow.png'), dark_image=Image.open('../../assets/arrow.png'), size=(20, 20))
        login_btn = ctk.CTkButton(master=wrap_controls, text='Đăng nhập', width=10, fg_color=Utils.BLUE, text_color="white", font=('', 18, 'bold'), image=my_image, compound='left',
                                  command=lambda: self.on_login_click(username_ent.get(), password_ent.get()))

        wrap_controls.pack(side=tk.TOP, expand=tk.YES, padx=50, pady=50)
        login_btn.pack(side=tk.TOP, fill='none', expand=tk.NO, pady=30)
        login_form.pack(side='left', expand=tk.YES, fill=tk.BOTH)
        parent.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

    def on_login_click(self, username, password):
        user: User
        if username == "" or password == "":
            tkMessageBox.showinfo("Cảnh báo", "Cập nhật đầy đủ thông tin trước khi đăng nhập!")
        else:
            user = self.__controller.login(username, password)
            if user is None:
                return
            self.__login_page.pack_forget()
            homepage = HomeView(self.__parent)
            # tab_controls = TabControls(self.__parent)


if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    root.state('zoomed')  # full screen
    root.resizable(True, True)
    root.iconbitmap('../../assets/restaurant.ico')
    root.title("Restaurant Information")

    view = LoginView(root)
    root.mainloop()
