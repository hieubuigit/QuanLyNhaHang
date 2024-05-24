import tkinter.messagebox as msgBox
import bcrypt

from admin.login.login_model import LoginModel

class LoginController:
    def __init__(self):
        self.__user_model = LoginModel()

    def login(self, username, password):
        user = self.__user_model.get_user_by_user_name(username)
        if user.password == '':
            msgBox.showerror("Lỗi", 'Tên tài khoản hoặc mật khẩu của bạn không đúng!')
        isPass = bcrypt.checkpw(bytes(password, encoding="utf8"), bytes(user.password, encoding="utf8"))
        if isPass:
            msgBox.showinfo("Đăng nhập", 'Đăng nhập thành công!')
            user_profile = user
        else:
            msgBox.showerror("Lỗi", 'Tên tài khoản hoặc mật khẩu của bạn không đúng!')

