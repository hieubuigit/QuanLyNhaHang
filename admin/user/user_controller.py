import tkinter.messagebox as msgBox
import bcrypt

from admin.user.user_model import *


class UserController:
    def __init__(self):
        self.__user_model = UserModel()

    def login(self, username, password):
        password_hashed = self.__user_model.get_password_hash(username)
        if password_hashed == '':
            msgBox.showerror("Lỗi", 'Tên tài khoản hoặc mật khẩu của bạn không đúng!')
        isPass = bcrypt.checkpw(bytes(password, encoding="utf8"), bytes(password_hashed, encoding="utf8"))
        if isPass:
            msgBox.showinfo("Đăng nhập", 'Đăng nhập thành công!')
        else:
            msgBox.showerror("Lỗi", 'Tên tài khoản hoặc mật khẩu của bạn không đúng!')
