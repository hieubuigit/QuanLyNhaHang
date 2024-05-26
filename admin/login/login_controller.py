import tkinter.messagebox as msgBox
import bcrypt

from admin.login.login_model import LoginModel
from share.utils import Utils


class LoginController:
    def __init__(self):
        self.__user_model = LoginModel()

    def login(self, username, password):
        try:
            user = self.__user_model.get_user_by_user_name(username)
            if user.password == '':
                msgBox.showerror("Lỗi", 'Tên tài khoản hoặc mật khẩu của bạn không đúng!')
                return None
            isPass = bcrypt.checkpw(bytes(password, encoding="utf8"), bytes(user.password, encoding="utf8"))
            if isPass:
                Utils.user_profile = user
                return user
            else:
                msgBox.showerror("Lỗi", 'Tên tài khoản hoặc mật khẩu của bạn không đúng!')
                return None
        except Exception as ex:
            print(ex)
            return None

