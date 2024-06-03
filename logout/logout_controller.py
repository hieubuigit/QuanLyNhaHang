import tkinter.messagebox as tkMsgBox

from login.login_controller import LoginController
from share.utils import Utils


class LogoutController:
    def __init__(self):
        self.__login_controller = LoginController()

    def logout(self, parent):
        Utils.user_profile = {}
        self.__login_controller.open_page(parent)
