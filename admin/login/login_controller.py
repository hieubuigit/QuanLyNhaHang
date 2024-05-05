import tkinter.messagebox as msgBox
import bcrypt

from admin.login.login_model import LoginModel
from share.utils import *


class LoginController:
    def __init__(self):
        self.__user_model = LoginModel()

    def login(self, username, password):
        user = self.__user_model.get_password_hash(username)
        password_hashed = user[12]
        if password_hashed == '':
            msgBox.showerror("Lỗi", 'Tên tài khoản hoặc mật khẩu của bạn không đúng!')
        isPass = bcrypt.checkpw(bytes(password, encoding="utf8"), bytes(password_hashed, encoding="utf8"))
        if isPass:
            msgBox.showinfo("Đăng nhập", 'Đăng nhập thành công!')
            user_profile = user
        else:
            msgBox.showerror("Lỗi", 'Tên tài khoản hoặc mật khẩu của bạn không đúng!')

