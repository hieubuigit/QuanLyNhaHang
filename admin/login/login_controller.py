import tkinter.messagebox as msgBox
import bcrypt

from admin.login.login_model import LoginModel
from share.common_config import UserStatus
from share.utils import Utils


class LoginController:
    def __init__(self):
        self.__user_model = LoginModel()

    def login(self, username, password):
        try:
            user_is_exist = self.__user_model.is_exist(username)
            if user_is_exist == False:
                msgBox.showerror("Lỗi", 'Tên tài khoản hoặc mật khẩu của bạn không đúng!')
                return
            user = self.__user_model.get_user_by_user_name(username)
            if user.status == UserStatus.INACTIVE.value:
                msgBox.showerror("Lỗi", 'Tên tài khoản hiện đang khoá vui lòng liên hệ admin!')
                return None
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

