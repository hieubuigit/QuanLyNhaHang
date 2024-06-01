import tkinter.messagebox as msgBox
import bcrypt
from login.login_model import LoginModel
from share.common_config import UserStatus, UserType
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
                user_profile = {
                    "user_code": user.user_code,
                    "type": user.type,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                }
                Utils.user_profile = user_profile
                return user
            else:
                msgBox.showerror("Lỗi", 'Tên tài khoản hoặc mật khẩu của bạn không đúng!')
                return None
        except Exception as ex:
            print(ex)
            return None

    @staticmethod
    def is_have_permission():
        is_allow = False
        if Utils.user_profile is not None:
            if Utils.user_profile["type"] == UserType.ADMIN.value:
                is_allow = True
        return is_allow
