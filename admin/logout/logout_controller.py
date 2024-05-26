import tkinter.messagebox as tkMsgBox
# import tkinter as tk


class LogoutController:
    def logout(self):
        response = tkMsgBox.askyesno("Thông báo", "Bạn có muốn đăng xuất?")
        if response:
            print("Đăng xuất thành công! Chuyển về page login")
        else:
            print("Hide confirm")
